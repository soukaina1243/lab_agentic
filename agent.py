from langchain_ollama import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession
from mcp.client.sse import sse_client
import asyncio
import json
import nest_asyncio

nest_asyncio.apply()

MCP_SERVERS = {
    "destination": "http://127.0.0.1:3001/sse",
    "budget":      "http://127.0.0.1:3002/sse",
    "weather":     "http://127.0.0.1:3003/sse",
    "currency":    "http://127.0.0.1:3004/sse",
    "calculator":  "http://127.0.0.1:3005/sse",
}

async def call_tool_fresh(server_url: str, tool_name: str, kwargs: dict) -> str:
    """Open a fresh SSE session, call the tool, then close it."""
    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            for t in tools:
                if t.name == tool_name:
                    result = await t.arun(kwargs)
                    return result
    return f"Tool '{tool_name}' not found on server."

async def get_tool_schemas():
    """Load tool metadata (names, params) once at startup."""
    tools_info = []
    for server_name, url in MCP_SERVERS.items():
        async with sse_client(url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await load_mcp_tools(session)
                for t in tools:
                    schema = t.args_schema
                    if isinstance(schema, dict):
                        props = schema.get("properties", {})
                    else:
                        try:
                            props = schema.schema().get("properties", {})
                        except Exception:
                            props = {}
                    param_names = list(props.keys())
                    param_types = {k: v.get("type", "string") for k, v in props.items()}
                    tools_info.append({
                        "name": t.name,
                        "description": t.description,
                        "server_url": url,
                        "param_names": param_names,
                        "param_types": param_types,
                    })
                    print(f"✅ Found tool: {t.name} → {param_names}")
    return tools_info

def build_tool(tool_info: dict) -> Tool:
    """Build a LangChain Tool that opens a fresh MCP session on every call."""
    name        = tool_info["name"]
    description = tool_info["description"]
    server_url  = tool_info["server_url"]
    param_names = tool_info["param_names"]
    param_types = tool_info["param_types"]

    def run_tool(input_str: str) -> str:
        input_str = input_str.strip().strip('"').strip("'")
        print(f"📨 [{name}] raw input: {input_str!r}")

        # Try JSON
        try:
            kwargs = json.loads(input_str)
            if isinstance(kwargs, dict):
                for k in kwargs:
                    if param_types.get(k) == "integer":
                        kwargs[k] = int(kwargs[k])
                    elif param_types.get(k) == "number":
                        kwargs[k] = float(kwargs[k])
                print(f"📨 [{name}] calling with (JSON): {kwargs}")
                loop = asyncio.get_event_loop()
                return loop.run_until_complete(
                    call_tool_fresh(server_url, name, kwargs)
                )
        except (json.JSONDecodeError, TypeError):
            pass

        # Comma-separated
        parts = [p.strip() for p in input_str.split(",")]
        kwargs = {}
        for i, pname in enumerate(param_names):
            val = parts[i].strip() if i < len(parts) else ""
            if param_types.get(pname) == "integer":
                try:
                    val = int(val)
                except ValueError:
                    pass
            elif param_types.get(pname) == "number":
                try:
                    val = float(val)
                except ValueError:
                    pass
            kwargs[pname] = val

        print(f"📨 [{name}] calling with (parsed): {kwargs}")
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(
                call_tool_fresh(server_url, name, kwargs)
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"Tool error: {str(e)}"

    return Tool(
        name=name,
        description=description + f" | params: {', '.join(param_names)}",
        func=run_tool,
    )

def run_travel_agent(user_request: str) -> tuple:
    loop = asyncio.get_event_loop()

    # Load only metadata at startup
    tools_info = loop.run_until_complete(get_tool_schemas())

    if not tools_info:
        return "❌ No tools found. Make sure all MCP servers are running.", []

    # Build tools that open fresh sessions per call
    tools = [build_tool(info) for info in tools_info]

    llm = ChatOllama(model="llama3.2", temperature=0)

    prompt = PromptTemplate.from_template("""
You are a helpful travel planning agent. Use the available tools to answer.

Tools:
{tools}

Tool names: {tool_names}

STRICT format to follow:

Question: the input question
Thought: what I need to do
Action: tool_name
Action Input: input value (see rules below)
Observation: tool result
... (repeat as needed)
Thought: I now have all the information
Final Answer: full travel plan

Input rules (no quotes, no JSON, plain text only):
- search_destination → city name only. Example: Barcelona
- estimate_budget → city,days. Example: Barcelona,5
- get_weather → city,month. Example: Barcelona,June
- convert_currency → amount,from,to. Example: 750,USD,EUR
- calculate → math expression. Example: 150 * 5

Begin!

Question: {input}
Thought:{agent_scratchpad}
""")

    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=15,
        return_intermediate_steps=True
    )

    response = executor.invoke({"input": user_request})

    tool_log = []
    for step in response.get("intermediate_steps", []):
        action, observation = step
        tool_log.append({
            "tool": action.tool,
            "input": action.tool_input,
            "output": observation
        })

    return response["output"], tool_log