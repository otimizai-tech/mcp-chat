# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

from langchain_openai import ChatOpenAI
import asyncio

async def run():
    model = ChatOpenAI(
                model="google/gemini-2.0-pro-exp-02-05:free",
                base_url="https://openrouter.ai/api/v1",
                api_key="sk-or-v1-dc7fb764058127c802asdasd3ce0095ab078d515f5ba708531aeafdd56a"
            )

    server_params = StdioServerParameters(
        command="python",
        # Mantive o caminho original do seu arquivo
        args=["/Users/flavioovatsug/Desktop/otimizai/bot/copilot/backend/langchain_mcp/math_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({
                "messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]
            })
            
            print("Resposta do agente:", agent_response)
            return agent_response

# Para executar a função assíncrona
if __name__ == "__main__":
    asyncio.run(run())