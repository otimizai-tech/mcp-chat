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
            {
                "name": tool.name,
                "description": tool.description,
                "schema": tool.inputSchema,
            }
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


'''
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastmcp import FastMCP
import asyncio
import json

app = FastAPI()
mcp = FastMCP("Teste")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Soma dois números"""
    print(f"Executando soma: {a} + {b}")
    result = a + b
    print(f"Resultado: {result}")
    return result

@mcp.tool()
def to_uppercase(text: str) -> str:
    """Converte texto para maiúsculas"""
    print(f"Convertendo para maiúsculas: {text}")
    result = text.upper()
    print(f"Resultado: {result}")
    return result

@app.get("/mcp")
@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Endpoint unificado para o MCP que lida com list_tools e call_tool"""
    print(f"\n=== Requisição {request.method} recebida em /mcp ===")
    print(f"Headers: {dict(request.headers)}")
    
    if request.method == "GET":
        # Listar ferramentas (antigo /mcp/tools)
        accept = request.headers.get("accept", "")
        print(f"Accept header: {accept}")
        
        tools = await mcp.list_tools()
        print(f"\nFerramentas disponíveis: {[t.name for t in tools]}")
        
        tools_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "tools": [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "schema": tool.inputSchema,
                    }
                    for tool in tools
                ]
            }
        }
        
        if "text/event-stream" in accept:
            print("Retornando resposta SSE")
            async def event_stream():
                data = json.dumps(tools_data)
                print(f"Enviando dados: {data}")
                yield f"data: {data}\n\n"
                
            return StreamingResponse(
                event_stream(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }
            )
        else:
            print("Retornando resposta JSON")
            return JSONResponse(content=tools_data)
            
    elif request.method == "POST":
        # Chamar ferramenta (antigo /mcp/call-tool)
        data = await request.json()
        print(f"Dados recebidos: {data}")
        
        name = data.get("name")
        arguments = data.get("arguments", {})

        if not name:
            print("Erro: nome da ferramenta não fornecido")
            raise HTTPException(status_code=400, detail="O nome da ferramenta é obrigatório")

        try:
            print(f"Chamando ferramenta {name} com argumentos {arguments}")
            result = await mcp.call_tool(name, arguments)
            print(f"Resultado: {result}")
            
            response = {

                "result": {
                    "tool": name,
                    "result": result
                }
            }
            print(f"Retornando resposta: {response}")
            return response
        except Exception as e:
            print(f"Erro ao executar ferramenta: {e}")
            return {
                "error": {
                    "code": -32000,
                    "message": str(e)
                }
            }

if __name__ == "__main__":
    print("\n=== Iniciando servidor MCP ===")
    print("Ferramentas disponíveis:")
    print("- add(a: int, b: int) -> int")
    print("- to_uppercase(text: str) -> str")
    print("\nServidor rodando em http://localhost:8001")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

'''