import asyncio
import nest_asyncio
nest_asyncio.apply()

from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession
from mcp.client.sse import sse_client

async def test():
    async with sse_client("http://127.0.0.1:3001/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            tool = tools[0]
            print(f"Testing: {tool.name}")
            result = await tool.arun({"destination": "Paris"})
            print(f"Result: {result}")

asyncio.run(test())
