
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

async def run_agent_queries():
    model = ChatOpenAI(
                model="google/gemini-2.0-pro-exp-02-05:free",
                base_url="https://openrouter.ai/api/v1",
                api_key="sk-or-v1-dc7fb764058127c802asdasd3ce0095ab078d515f5ba708531aeafdd56a"
            )
    async with MultiServerMCPClient(
        {

            "weather": {
                # make sure you start your weather server on port 8000
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    ) as client:
        agent = create_react_agent(model, client.get_tools())
        math_response = await agent.ainvoke({"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]})
        print("Math response:", math_response)
        
        weather_response = await agent.ainvoke({"messages": [{"role": "user", "content": "what is the weather in nyc?"}]})
        print("Weather response:", weather_response)

# To run this async function, you need to use asyncio
import asyncio

# This is the entry point when running as a script
if __name__ == "__main__":
    asyncio.run(run_agent_queries())