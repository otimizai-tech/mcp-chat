"""
This is the main entry point for the agent.
It defines the workflow graph, state, tools, nodes and edges.
"""

from typing_extensions import Literal, TypedDict, Dict, List, Any, Union, Optional
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from copilotkit import CopilotKitState
from langchain_mcp_adapters.client import MultiServerMCPClient
import os

# Define the connection type structures
class StdioConnection(TypedDict):
    command: str
    args: List[str]
    transport: Literal["stdio"]

class SSEConnection(TypedDict):
    url: str
    transport: Literal["sse"]

MCPConfig = Dict[str, Union[StdioConnection, SSEConnection]]

class AgentState(CopilotKitState):
    """
    Defines the state of the agent, including optional MCP configuration.
    """
    mcp_config: Optional[MCPConfig]

DEFAULT_MCP_CONFIG: MCPConfig = {
    "math": {
        "command": "python",
        "args": [os.path.join(os.path.dirname(__file__), "..", "math_server.py")],
        "transport": "stdio",
    },
}

async def chat_node(state: AgentState, config: RunnableConfig) -> Command[Literal["__end__"]]:
    """
    Uses OpenRouter as the LLM instead of a ReAct agent.
    """
    mcp_config = state.get("mcp_config", DEFAULT_MCP_CONFIG)

    print(f"mcp_config: {mcp_config}, default: {DEFAULT_MCP_CONFIG}")
    
    async with MultiServerMCPClient(mcp_config) as mcp_client:
        mcp_tools = mcp_client.get_tools()
        
        model = ChatOpenAI(
            model="google/gemini-2.5-pro-exp-02-05:free",  
            openai_api_key="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",  
            openai_api_base="https://openrouter.ai/api/v1"  
        )

        agent_input = {
            "messages": state["messages"]
        }
        
        agent_response = await model.ainvoke(agent_input)
        
        updated_messages = state["messages"] + agent_response.get("messages", [])
        
        return Command(
            goto=END,
            update={"messages": updated_messages},
        )

# Definir o workflow graph
workflow = StateGraph(AgentState)
workflow.add_node("chat_node", chat_node)
workflow.set_entry_point("chat_node")

# Compilar o workflow graph
graph = workflow.compile(MemorySaver())
