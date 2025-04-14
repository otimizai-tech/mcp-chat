from fastapi import FastAPI
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
from mcp_client import graph


app = FastAPI()
sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAgent(
            name="mcp_agent",
            description="This agent uses mcp servers to run tools and can interact with UI actions",
            graph=graph,
        )
    ],
)

add_fastapi_endpoint(app, sdk, "/copilotkit")

def main():
    """Run the uvicorn ."""
    import uvicorn
    uvicorn.run("dev_server:app", host="0.0.0.0", port=8002, reload=True)
 
if __name__ == "__main__":
    main()