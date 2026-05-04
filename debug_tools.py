import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession
from mcp.client.sse import sse_client

async def debug():
    async with sse_client("http://127.0.0.1:3002/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            for t in tools:
                print(f"Tool name: {t.name}")
                print(f"Args schema: {t.args_schema}")
                try:
                    print(f"Schema dict: {t.args_schema.schema()}")
                except Exception as e:
                    print(f"Schema error: {e}")
                try:
                    print(f"Model fields: {t.args_schema.model_fields}")
                except Exception as e:
                    print(f"Fields error: {e}")

asyncio.run(debug())