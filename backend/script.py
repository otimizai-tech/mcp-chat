# tirado daqui: https://github.com/modelcontextprotocol/python-sdk/tree/6b6f34eaa638c08f80a432c3627cc78b778a0ad2?tab=readme-ov-file#writing-mcp-clients


# typescript # https://github.com/modelcontextprotocol/typescript-sdk
# adapter https://github.com/langchain-ai/langchain-mcp-adapters



from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="uv",  # Executable
    args=["run","--with" ,"fastmcp" ,"fastmcp", "run", "/Users/flavioovatsug/Desktop/otimizai/bot/copilot/backend/mcp/server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)

# fastapi # sse http post (json-rpc) localhost:8000 -->  json = {"jsonrpc": "2.0", "method": "add", "params": {"a": 1, "b": 2}, "id": 1}
# https://spec.modelcontextprotocol.io/specification/draft/basic/authorization/#232-authorization-base-url


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            resources = await session.list_resources()
            tools = await session.list_tools()
            
            result = await session.call_tool("add", arguments={"a": 1, "b": 2})
            # print(result)
            # print(str(tools))
            
            print(resources)
            print(tools.tools[0].name)
            print(tools.tools[0].description)
            print(tools.tools[0].inputSchema)
                        # Call a tool
            # print(resources)



if __name__ == "__main__":
    import asyncio

    asyncio.run(run())