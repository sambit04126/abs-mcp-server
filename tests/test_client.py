import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

async def test_abs_server():
    server_params = StdioServerParameters(
        command="python",
        args=["src/abs_mcp_server/server.py"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test search
            result = await session.call_tool(
                "search_datasets", 
                arguments={"keyword": "census", "limit": 2}
            )
            print("Search result:", result.content)

if __name__ == "__main__":
    asyncio.run(test_abs_server())