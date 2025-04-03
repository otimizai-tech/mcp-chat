from mcp.server.fastmcp import FastMCP
import asyncio

mcp = FastMCP("teste")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Soma dois números"""
    return a + b

@mcp.tool()
def to_uppercase(text: str) -> str:
    """Converte texto para maiúsculas"""
    return text.upper()

if __name__ == "__main__":
    asyncio.run(mcp.run(transport="sse"))