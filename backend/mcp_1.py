from fastapi import FastAPI, HTTPException
from fastmcp import FastMCP
import asyncio

app = FastAPI()
mcp = FastMCP("Teste")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Soma dois números"""
    return a + b

@mcp.tool()
def to_uppercase(text: str) -> str:
    """Converte texto para maiúsculas"""
    return text.upper()

@app.get("/mcp/tools")
async def list_mcp_tools():
    """Lista as ferramentas registradas no MCP"""
    tools = await mcp.list_tools()  
    return {
        "tools": [
            {"name": tool.name, "description": tool.description, "schema": tool.inputSchema}
            for tool in tools
        ]
    }

@app.post("/mcp/call-tool")
async def call_mcp_tool(data: dict):
    """
    Chama uma ferramenta do MCP pelo nome e argumentos.
    """
    name = data.get("name")
    arguments = data.get("arguments", {})

    if not name:
        raise HTTPException(status_code=400, detail="O nome da ferramenta é obrigatório")

    try:
        result = await mcp.call_tool(name, arguments)
        return {"tool": name, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import threading
    import uvicorn

    def run_mcp():
        asyncio.run(mcp.run(transport="sse"))

    def run_api():
        uvicorn.run(app, host="0.0.0.0", port=8001)

    threading.Thread(target=run_mcp, daemon=True).start()
    run_api()