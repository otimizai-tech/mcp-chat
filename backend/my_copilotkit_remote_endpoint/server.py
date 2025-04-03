from fastapi import FastAPI
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, Action as CopilotAction
from fastapi.middleware.cors import CORSMiddleware

 
app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize the CopilotKit SDK
sdk = CopilotKitRemoteEndpoint()
 
# Add the CopilotKit endpoint to your FastAPI app
add_fastapi_endpoint(app, sdk, "/copilotkit_remote")
    
def main():
    """Run the uvicorn server."""
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)
 
if __name__ == "__main__":
    main()