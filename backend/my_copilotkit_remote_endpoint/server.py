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

# Define your backend action
async def fetch_name_for_user_id(userId: str):
    # Replace with your database logic
    return {"name": "User_" + userId}
 
# this is a dummy action for demonstration purposes
action = CopilotAction(
    name="fetchNameForUserId",
    description="Fetches user name from the database for a given ID.",
    parameters=[
        {
            "name": "userId",
            "type": "string",
            "description": "The ID of the user to fetch data for.",
            "required": True,
        }
    ],
    handler=fetch_name_for_user_id
)
 
# Initialize the CopilotKit SDK
sdk = CopilotKitRemoteEndpoint(actions=[action])
 
# Add the CopilotKit endpoint to your FastAPI app
add_fastapi_endpoint(app, sdk, "/copilotkit_remote")
    
def main():
    """Run the uvicorn server."""
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
 
if __name__ == "__main__":
    main()