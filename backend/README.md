# MCP Server

Este é um servidor FastMCP que fornece ferramentas básicas de processamento através de uma API.

A ideia desse servidor é para que tenhamos rodando na porta 8000 (padrão do SSE) com as diferentes tools para utilizarmos no nosso agente

## Funcionalidades

No momento, o servidor disponibiliza as seguintes funções para teste:

### add(a: int, b: int) -> int

Função para somar dois números inteiros.

**Parâmetros:**

- a: primeiro número inteiro
- b: segundo número inteiro

**Retorno:**

- Soma dos dois números

**Exemplo:**

```python
resultado = add(5, 3)  # retorna 8 conforme o mcp previu
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

O servidor será iniciado com o nome "teste" e estará pronto para receber requisições do agente, em MCP Client

# MCP Client

O cliente MCP (`mcp_client.py`) é uma implementação que utiliza Server-Sent Events (SSE) para se comunicar com o servidor MCP. Basicamente é aqui aonde está sendo configurado o nosso agente LangGraph, onde ele tem acesso a todas as tools do MCP e actions do copilot

### Lógica utilizada

A principal ideia era integrar o MCP com o CopilotKit. Para isso, a solução mais adequada foi utilizar um agente LangGraph, que pudesse interagir tanto com qualquer ferramenta do MCP, quanto com qualquer ação do CopilotKit. Para viabilizar essa integração, utilizamos o self-hosting — ou seja, rodamos nossa própria API, que foi implementada no arquivo (`dev_server.py`), ao invés do cloud do CopilotKit.

### Características

- Utiliza LangChain e LangGraph para processamento
- Suporta integração com Azure OpenAI ou OpenRouter
- Implementa um sistema de estado baseado em grafos
- Usa Server-Sent Events para comunicação com o servidor
- Suporta actions do CopilotKit

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

# Dev Server

O Dev Server (`dev_server.py`) é um servidor FastAPI que atua como ponto de integração entre o CopilotKit e nosso agente MCP. Este servidor é fundamental para permitir a comunicação entre o nosso agente backend e o CopilotKit.

### Lógica utilizada

Para o CopilotKit funcionar, ele precisa de um aquivo de configuração no backend, então é por isso que esse arquivo é tão importante, ja que ele faz essa ligação do nosso client (rodando o agente LangGraph), para rodar em um endpoint que será acessado no nosso frontend.

### Características Principais

- Implementa um servidor FastAPI para desenvolvimento
- Integra o CopilotKit com nosso agente personalizado
- Fornece endpoints para comunicação com o frontend
- Suporta hot-reload para desenvolvimento

### Configuração

O servidor é configurado com:

```python
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
```

### Endpoint

O servidor expõe um endpoint principal:

- `/copilotkit`: Ponto de entrada para todas as interações do CopilotKit

### Como Executar

Para iniciar o servidor de desenvolvimento:

```bash
python dev_server.py
```

O servidor será iniciado em:

- Host: 0.0.0.0
- Porta: 8002
- Modo: Desenvolvimento (com hot-reload ativado)

### Integração

O Dev Server trabalha em conjunto com:

- MCP Server (porta 8000): fornece as ferramentas via SSE
- Frontend do CopilotKit: interface do usuário
- Agente LangGraph: processamento de linguagem natural


# Docker

O projeto utiliza Docker para containerização dos serviços, facilitando a implantação e garantindo consistência entre ambientes de desenvolvimento e produção.

### Arquitetura Docker

O sistema é composto por dois serviços principais:

1. **MCP Server (porta 8000)**

   - Serviço que fornece as ferramentas via SSE
   - Container: `mcp_server`
   - Comando: `python mcp_server.py`
   - Volumes: Monta o diretório atual em `/app`

2. **Dev Server (porta 8002)**
   - Serviço que integra o CopilotKit
   - Container: `dev_server`
   - Comando: `python dev_server.py`
   - Depende do `mcp_server`
   - Volumes: Monta o diretório atual em `/app`

### Rede

- Nome: `otimizai_network`
- Tipo: bridge
- Permite comunicação entre os containers

### Como Executar com Docker

Para iniciar todos os serviços:

```bash
docker-compose up --build
```

Para iniciar em background:

```bash
docker-compose up -d
```

Para parar os serviços:

```bash
docker-compose down
```

### Volumes

Ambos os serviços montam o diretório atual (`.`) no caminho `/app` dentro dos containers, permitindo:

- Desenvolvimento em tempo real
- Persistência de dados
- Hot-reload das alterações

# Gitingest Server

O `gitingest_server.py` é um servidor FastAPI que expõe a funcionalidade de ingestão Git através de uma API REST. Este servidor facilita a ingestão de repositórios remotos ou locais através de endpoints HTTP.

## Funcionalidades

- Endpoint REST para ingestão de repositórios Git
- Suporte a padrões de inclusão/exclusão de arquivos
- Processamento de URLs do GitHub com formato de árvore (tree)
- Extração automática de sumários, estrutura de arquivos e conteúdo

## Endpoints Principais

### GET /

Endpoint de verificação de saúde, retorna uma mensagem se o servidor estiver funcionando.

### POST /ingest

Endpoint principal para ingestão de repositórios.

**Parâmetros da Requisição:**

```json
{
  "url": "string",                  // URL ou caminho do repositório (obrigatório)
  "include_patterns": ["string"],   // Padrões de arquivo a incluir (opcional)
  "exclude_patterns": ["string"],   // Padrões de arquivo a excluir (opcional)
  "branch": "string"                // Nome do branch a ser usado (opcional)
}
```

**Resposta:**

```json
{
  "summary": {},   // Resumo do repositório
  "tree": {},      // Estrutura de arquivos em árvore
  "content": {}    // Conteúdo dos arquivos
}
```

## Como Executar

O servidor está presente no docker também, mas caso queira rodar o arquivo de forma independente, basta executar o comando abaixo:

```bash
python gitingest_server.py
```

O servidor será iniciado em:
- Host: 0.0.0.0
- Porta: 8003

## Exemplo de Uso

A ingestão pode ser realizada através de requisição HTTP:

```bash
curl -X POST http://localhost:8003/ingest \
-H "Content-Type: application/json" \
-d '{
  "url": "link_do_repositório"
}'
```

### Recursos Avançados

- **URLs com Formato Tree**: O servidor processa automaticamente URLs do GitHub com formato `/tree/branch/path`
- **Inclusão Automática**: Arquivos markdown (*.md) são sempre incluídos, independentemente dos filtros
- **Filtragem de Diretórios**: Suporte para processar apenas subdiretórios específicos de um repositório