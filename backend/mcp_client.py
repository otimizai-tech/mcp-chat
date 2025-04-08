#%%
"""
Implementação adaptada do agent.py usando apenas conexão SSE
com as ferramentas do server.py
"""

from typing import Literal, Dict, List, Union, Optional
from typing_extensions import TypedDict
from langchain_openai import AzureChatOpenAI
#from langchain_openai import ChatOpenAI # Se for usar o openrouter
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langgraph.types import Command
from copilotkit import CopilotKitState
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

import os
import json

# Import Azure configurations from azure.py
from azure import (
    AZURE_OPENAI_ENDPOINT,
    DEPLOYMENT_NAME,
    API_VERSION,
    API_KEY
)

# Define a estrutura de conexão SSE
class SSEConnection(TypedDict):
    url: str
    transport: Literal["sse"]

# Tipo para configuração MCP (apenas SSE)
MCPConfig = Dict[str, SSEConnection]

class AgentState(CopilotKitState):
    """Define o estado do agente."""
    mcp_config: Optional[MCPConfig]

# Configuração MCP padrão usando SSE
DEFAULT_MCP_CONFIG: MCPConfig = {
    "tools": {
        "url": "http://localhost:8000/sse",
        "transport": "sse"
    }
}

'''
llm = ChatOpenAI(
    model="google/gemini-2.0-flash-001",  
    openai_api_key="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",  
    openai_api_base="https://openrouter.ai/api/v1"
)
'''

llm = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=DEPLOYMENT_NAME,
    api_version=API_VERSION,
    api_key=API_KEY,
    temperature=0.7,
    max_tokens=800
)


async def chat_node(state: AgentState, config: RunnableConfig) -> Command[Literal["__end__"]]:
    """Nó de chat que processa mensagens e executa ferramentas."""
    print("\n=== Iniciando processamento do chat ===")
    
    # Obtém configuração MCP do estado ou usa a configuração padrão
    mcp_config = state.get("mcp_config", DEFAULT_MCP_CONFIG)
    print(f"Configuração MCP: {mcp_config}")
    
    # Processa a mensagem usando o MultiServerMCPClient
    async with MultiServerMCPClient(mcp_config) as mcp_client:
        try:
            # Obtém as ferramentas
            print("Obtendo ferramentas do servidor...")
            mcp_tools = mcp_client.get_tools()
            print(f"Ferramentas disponíveis: {[t.name for t in mcp_tools]}")
            
            # Cria o agente
            agent = create_react_agent(llm, mcp_tools)
            
            # Prepara mensagens para o agente
            agent_input = {
                "messages": state["messages"]
            }
            print(f"Mensagens para o agente: {agent_input}")
            
            # Executa o agente
            print("Executando agente...")
            agent_response = await agent.ainvoke(agent_input)
            print(f"Resposta do agente: {agent_response}")
            
            # Atualiza as mensagens no estado
            updated_messages = state["messages"] + agent_response.get("messages", [])
            
            # Retorna comando para finalizar com mensagens atualizadas
            return Command(
                goto=END,
                update={"messages": updated_messages},
            )
            
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
            import traceback
            print(f"Stack trace:\n{traceback.format_exc()}")
            return Command(
                goto=END,
                update={"error": str(e)}
            )

# Define o grafo de fluxo de trabalho
workflow = StateGraph(AgentState)
workflow.add_node("chat", chat_node)
workflow.set_entry_point("chat")
workflow.add_edge("chat", END)
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

# Compila o grafo
# graph = workflow.compile()

# def serialize_response(obj):
#     """Serializa objetos para formato JSON."""
#     if hasattr(obj, "content"):
#         return {"content": obj.content, "type": obj.__class__.__name__}
#     if isinstance(obj, dict):
#         return {k: serialize_response(v) for k, v in obj.items()}
#     if isinstance(obj, list):
#         return [serialize_response(item) for item in obj]
#     return obj

# if __name__ == "__main__":
#     import asyncio
#     from langchain_core.messages import HumanMessage
    
#     async def test_agent():
#         """Testa o agente com uma mensagem simples"""
#         print("\n=== Iniciando teste do agente ===")
        
#         # Define o estado inicial
#         state = AgentState(
#             messages=[
#                 HumanMessage(content="Quanto é 2 + 2? E depois converta 'teste' para maiúsculas.")
#             ],
#             mcp_config=DEFAULT_MCP_CONFIG
#         )

#         print(state)
        
#         try:
#             # Executa o agente
#             print("\nExecutando o agente...")
#             response = await graph.ainvoke(state)
            
#             # Imprime a resposta
#             print("\n=== Resposta final do agente ===")
#             serialized_response = serialize_response(response)
#             print(json.dumps(serialized_response, indent=2, ensure_ascii=False))
#         except Exception as e:
#             print(f"\nErro ao executar o agente: {e}")
#             import traceback
#             print(f"Stack trace:\n{traceback.format_exc()}")
            
#     # Executa o teste
#     asyncio.run(test_agent())
# # %%

# %%
