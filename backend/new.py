from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from typing_extensions import Literal, TypedDict, Dict, List, Any, Union, Optional
import os

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from langchain_mcp_adapters.client import MultiServerMCPClient
from copilotkit import CopilotKitState

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StdioConnection(TypedDict):
    command: str
    args: List[str]
    transport: Literal["stdio"]

class SSEConnection(TypedDict):
    url: str
    transport: Literal["sse"]

MCPConfig = Dict[str, Union[StdioConnection, SSEConnection]]

class AgentState(CopilotKitState):
    """Estado do agente que mantém o histórico de mensagens e configurações MCP."""
    mcp_config: Optional[MCPConfig]

DEFAULT_MCP_CONFIG: MCPConfig = {
    "Teste": {
        "url": "http://localhost:8765/sse", 
        "transport": "sse",
    },
}

# LLM setup
llm = ChatOpenAI(
    model="google/gemini-2.5-pro-exp-03-25:free",  
    openai_api_key="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",  
    openai_api_base="https://openrouter.ai/api/v1"  
)

async def chat_node(state: AgentState, config: RunnableConfig) -> Command[Literal["__end__"]]:
    """
    Nó principal de processamento que executa o ReAct agent como subgrafo.
    Usa o MultiServerMCPClient para integrar ferramentas externas.
    """
    mcp_config = state.get("mcp_config", DEFAULT_MCP_CONFIG)
    
    async with MultiServerMCPClient(mcp_config) as mcp_client:
        mcp_tools = mcp_client.get_tools()
        
        from langgraph.prebuilt import create_react_agent
        react_agent = create_react_agent(model=llm, tools=mcp_tools)
        
        agent_input = {
            "messages": state["messages"]
        }
        
        agent_response = await react_agent.ainvoke(agent_input)
        updated_messages = state["messages"] + agent_response.get("messages", [])
        
        return Command(
            goto=END,
            update={"messages": updated_messages},
        )

# Definir o grafo de workflow
workflow = StateGraph(AgentState)
workflow.add_node("chat_node", chat_node)
workflow.set_entry_point("chat_node")

# Compilar o grafo de workflow (versão simplificada sem checkpoints)
graph = workflow.compile()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    mcp_config = data.get("mcp_config")
    
    # Criar estado inicial
    initial_state = {
        "messages": [HumanMessage(content=message)],
        "mcp_config": mcp_config or DEFAULT_MCP_CONFIG
    }
    
    # Executar o grafo
    final_state = await graph.ainvoke(initial_state)
    
    # Extrair a última mensagem do AI
    ai_messages = [msg for msg in final_state["messages"] if isinstance(msg, AIMessage)]
    output = ai_messages[-1].content if ai_messages else "Não foi possível gerar uma resposta."
    
    return {"response": output}

@app.get("/mcp-services")
async def get_mcp_services():
    try:
        async with MultiServerMCPClient(DEFAULT_MCP_CONFIG) as mcp_client:
            services = {name: {"status": "available"} for name in DEFAULT_MCP_CONFIG.keys()}
            return {"services": services}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)