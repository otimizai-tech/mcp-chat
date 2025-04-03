# MCP Server

Este é um servidor FastMCP que fornece ferramentas básicas de processamento através de uma API.

## Funcionalidades

O servidor disponibiliza as seguintes funções:

### add(a: int, b: int) -> int

Função para somar dois números inteiros.

**Parâmetros:**

- a: primeiro número inteiro
- b: segundo número inteiro

**Retorno:**

- Soma dos dois números

**Exemplo:**

```python
resultado = add(5, 3)  # retorna 8
```

### to_uppercase(text: str) -> str

Função para converter texto para letras maiúsculas.

**Parâmetros:**

- text: texto a ser convertido

**Retorno:**

- Texto convertido para maiúsculas

**Exemplo:**

```python
resultado = to_uppercase("hello")  # retorna "HELLO"
```

## Como executar

O servidor utiliza Server-Sent Events (SSE) como protocolo de transporte.

Para iniciar o servidor, execute:

```bash
python mcp_server.py
```

O servidor será iniciado com o nome "teste" e estará pronto para receber requisições.

# MCP Client

O cliente MCP (`mcp_client.py`) é uma implementação que utiliza Server-Sent Events (SSE) para se comunicar com o servidor MCP.

### Características

- Utiliza LangChain e LangGraph para processamento
- Suporta integração com Azure OpenAI ou OpenRouter
- Implementa um sistema de estado baseado em grafos
- Usa Server-Sent Events para comunicação com o servidor

### Configuração do Modelo LLM

O cliente suporta dois modos de LLM, utilizando o openrouter ou o Azure OpenAI (padrão):

#### Azure OpenAI (Padrão)

```python
llm = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=DEPLOYMENT_NAME,
    api_version=API_VERSION,
    api_key=API_KEY,
    temperature=0.7,
    max_tokens=800
)
```

#### OpenRouter (Alternativo)

Para usar o OpenRouter em vez do Azure:

1. Comente o bloco de código do Azure OpenAI
2. Descomente o bloco do OpenRouter:

```python
llm = ChatOpenAI(
    model="google/gemini-2.0-flash-001",
    openai_api_key="sua-chave-aqui",
    openai_api_base="https://openrouter.ai/api/v1"
)
```

### Como executar

1. Certifique-se que o MCP Server está rodando
2. Execute o client com o comando:

```bash
python mcp_client.py
```

O cliente iniciará com um teste padrão que soma números e converte texto para maiúsculas.

### Configuração

O cliente usa uma configuração padrão para conexão SSE:

```python
DEFAULT_MCP_CONFIG = {
    "tools": {
        "url": "http://localhost:8000/sse",
        "transport": "sse"
    }
}
```
