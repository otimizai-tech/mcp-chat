from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
from pydantic import BaseModel, Field
import os
from litellm import completion

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


## Set ENV variables
os.environ["OPENROUTER_API_KEY"] = "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"

@app.post("/api/chat")
async def chat_endpoint(request: Request) -> JSONResponse:
    """
    Handles AI chat requests using LiteLLM
    """
    try:
        body = await request.json()
        
        if not body:
            raise HTTPException(status_code=400, detail="Prompt is required")

        parametros = body.get("parametros", "")
        mensagens = parametros.get("mensagens", [])
            
        response = completion(
            model="openrouter/google/gemini-2.5-pro-exp-03-25:free",
            messages=mensagens
        )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "response": response.choices[0].message.content
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": str(e)
            }
        )

    
@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4000)