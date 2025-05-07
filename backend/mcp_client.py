#%%
"""
Implementação adaptada do agent.py usando apenas conexão SSE
com as ferramentas MCP do server.py
"""

"""
MCP Client Implementation

Este módulo implementa um cliente MCP especializado que integra diferentes componentes:
1. Comunicação SSE (Server-Sent Events) para interação com servidores de ferramentas
2. Integração com LangChain e Azure OpenAI para processamento de linguagem natural
3. Sistema de gerenciamento de estado para copilot
4. Execução de ferramentas remotas via MCP

Principais funcionalidades:
- Estabelece conexão com servidores MCP via SSE
- Gerencia ferramentas remotas e ações do copilot
- Processa mensagens usando modelos de linguagem
- Executa ferramentas de forma assíncrona
- Implementa fallback para agente React em caso de falhas

O fluxo de trabalho é gerenciado através de um grafo de estados que:
1. Recebe mensagens do usuário
2. Processa usando LLM
3. Identifica e executa ferramentas mcp ou actions necessárias
4. Retorna respostas processadas

Este módulo é fundamental para a infraestrutura do copilot, servindo como ponte
entre a interface do usuário e os serviços de processamento de linguagem natural.
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
from langchain_core.messages import ToolMessage

import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Azure configurations from environment variables
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
DEPLOYMENT_NAME = os.getenv('AZURE_DEPLOYMENT_NAME')
API_VERSION = os.getenv('AZURE_API_VERSION')
API_KEY = os.getenv('AZURE_API_KEY')

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
        #"url": "http://localhost:8000/sse",
        "url": "http://mcp_server:8000/sse",
        "transport": "sse"
    }
}

'''
llm = ChatOpenAI(
    model="google/gemini-2.0-flash-001",  
    openai_api_key="your_key",  
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
    """Nó de chat que processa mensagens e executa ferramentas diretamente."""
    print("\n=== Iniciando processamento do chat ===")
    
    # Obtém configuração MCP do estado ou usa a configuração padrão
    mcp_config = state.get("mcp_config", DEFAULT_MCP_CONFIG)
    print(f"Configuração MCP: {mcp_config}")
    
    try:
        # Processa com MultiServerMCPClient para obter ferramentas MCP
        async with MultiServerMCPClient(mcp_config) as mcp_client:
            print("Obtendo ferramentas do servidor...")
            mcp_tools = mcp_client.get_tools()
            print(f"Ferramentas MCP disponíveis: {[t.name for t in mcp_tools]}")
            
            copilot_actions = state.get("copilotkit", {}).get("actions", [])
            print(f"Ações do Copilot disponíveis: {[a.get('name') for a in copilot_actions]}")
            
            model_with_tools = llm.bind_tools(
                [
                    *copilot_actions,
                    *mcp_tools,
                ]
            )
            
            print("Executando modelo com ferramentas combinadas...")
            response = await model_with_tools.ainvoke(
                state["messages"],
                config
            )
            print(f"Resposta do modelo: {response}")
            
            if hasattr(response, "tool_calls") and response.tool_calls:
                tool_name = response.tool_calls[0].get("name")
                print(f"Ferramenta chamada: {tool_name}")
                
                is_copilot_action = any(
                    action.get("name") == tool_name
                    for action in copilot_actions
                )
                
                if is_copilot_action:
                    print(f"Ação do Copilot detectada: {tool_name}. Finalizando.")
                    return Command(
                        goto=END,
                        update={"messages": state["messages"] + [response]},
                    )
                
                print(f"Executando ferramenta MCP: {tool_name} diretamente...")
                
                mcp_tool = [tool for tool in mcp_tools if tool.name == tool_name]
                
                if not mcp_tool:
                    print(f"Ferramenta {tool_name} não encontrada.")
                    error_message = {"content": f"A ferramenta solicitada '{tool_name}' não está disponível.", "type": "AIMessage"}
                    return Command(
                        goto=END, 
                        update={"messages": state["messages"] + [response, error_message]}
                    )
                
                try:
                    print(f"Executando ferramenta MCP {tool_name} via MCP client...")
                    
                    tool_call = response.tool_calls[0]
                    tool_args = tool_call.get("args", {})
                    tool_id = tool_call.get("id")
                    
                    # Executa a ferramenta via MCP
                    from langchain_core.messages import ToolMessage
                    tool_result = await mcp_client.run_tool(tool_name, tool_args)
                    print(f"Resultado da ferramenta: {tool_result}")
                    
                    # Cria uma mensagem de ferramenta com o resultado
                    tool_message = ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tool_id
                    )
                    
                    # Atualiza as mensagens com a resposta da ferramenta
                    updated_messages = state["messages"] + [response, tool_message]
                    
                    # Executa uma nova chamada ao LLM para processar o resultado da ferramenta
                    final_response = await llm.ainvoke(updated_messages, config)
                    
                    # Finaliza com a resposta completa
                    return Command(
                        goto=END,
                        update={"messages": updated_messages + [final_response]}
                    )
                    
                except Exception as tool_error:
                    print(f"Erro ao executar ferramenta diretamente: {tool_error}")
                    print("Tentando usar o agente reAct como fallback...")
                    
                    # Se der errado: Usar o agente reAct
                    tool_agent = create_react_agent(llm, mcp_tool)
                    
                    # Executa o agente com as mensagens originais
                    print(f"Executando agente React para a ferramenta {tool_name}...")
                    agent_input = {"messages": state["messages"]}
                    tool_response = await tool_agent.ainvoke(agent_input)
                    print(f"Resposta do agente React: {tool_response}")
                    
                    return Command(
                        goto=END,
                        update={"messages": state["messages"] + tool_response.get("messages", [])}
                    )
            
            # Se não houver chamadas de ferramentas, finaliza normalmente
            return Command(
                goto=END,
                update={"messages": state["messages"] + [response]},
            )
    
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")
        import traceback
        print(f"Stack trace:\n{traceback.format_exc()}")
        return Command(
            goto=END,
            update={"error": str(e)}
        )

# Define o grafo de fluxo de trabalho - muito mais simples agora
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
