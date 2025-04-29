"""
Servidor de Desenvolvimento para Integração Copilot

Este módulo implementa um servidor FastAPI que serve como ponto de integração
para o sistema Copilot. Suas principais responsabilidades incluem:

1. Configuração e Exposição de API:
   - Configura um servidor FastAPI
   - Expõe endpoints necessários para integração com o CopilotKit
   - Gerencia rotas e requisições HTTP

2. Integração com Agentes:
   - Integra o LangGraphAgent que utiliza servidores MCP
   - Permite comunicação bidirecional entre UI e ferramentas
   - Gerencia o ciclo de vida dos agentes

3. Desenvolvimento e Depuração:
   - Fornece ambiente de desenvolvimento com hot-reload
   - Facilita testes e depuração de integrações
   - Permite monitoramento de requisições e respostas

Este servidor é essencial para:
- Desenvolvimento e teste de novas funcionalidades
- Integração entre frontend e backend
- Gerenciamento de agentes e ferramentas
- Exposição de APIs para o CopilotKit

O servidor roda na porta 8002 e inclui recursos de desenvolvimento
como reload automático para facilitar o processo de desenvolvimento.
"""

from fastapi import FastAPI
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
from mcp_client import graph


app = FastAPI()
sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAgent(
            name="mcp_agent",
            description="This agent uses mcp servers to run tools and can interact with UI actions",
            graph=graph,
        )
    ],
)

add_fastapi_endpoint(app, sdk, "/copilotkit")

def main():
    """Run the uvicorn ."""
    import uvicorn
    uvicorn.run("dev_server:app", host="0.0.0.0", port=8002, reload=True)
 
if __name__ == "__main__":
    main()