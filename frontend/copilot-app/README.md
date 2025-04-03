# Aplicação Frontend Copilotkit chat

Este é um projeto [Next.js](https://nextjs.org) integrado com [CopilotKit](https://docs.copilotkit.ai/) para recursos de assistência com IA.

## Visão Geral do Projeto

Esta aplicação frontend combina Next.js com CopilotKit para criar uma interface potencializada por IA. Utiliza:

- Next.js como framework React
- CopilotKit para interações com IA
- Integração com OpenRouter API usando modelo Gemini
- Server-Side Events (SSE) para comunicação com backend

## Arquitetura

### Integração CopilotKit

A aplicação utiliza o runtime do CopilotKit com a seguinte configuração:

- Endpoint da API: `/api/copilotkit`
- Modelo: `google/gemini-2.5-pro-exp-03-25:free`
- OpenRouter como provedor da API
- Comunicação com backend através do `localhost:8001`

### Configuração da API

A API CopilotKit está configurada em `pages/api/copilotkit.ts` com:

- Integração OpenRouter
- Tratamento de erros
- Conexão com endpoint remoto do servidor backend

## Começando

1. Primeiro, instale as dependências:

```bash
npm install
# ou
yarn install
```

2. Execute o servidor de desenvolvimento:

```bash
npm run dev
# ou
yarn dev
```

A aplicação estará disponível em [http://localhost:3000](http://localhost:3000).

## Documentação da API

### Endpoint CopilotKit

O endpoint `/api/copilotkit` gerencia interações com IA com os seguintes recursos:

- Integração com OpenRouter API
- Comunicação com backend
- Tratamento e registro de erros

## Integração com Backend

O frontend se comunica com o servidor backend através de:

- URL: `http://localhost:8000/copilotkit_remote`
- Protocolo: Server-Sent Events (SSE)
- Configuração de runtime no manipulador CopilotKit

## Saiba Mais

- [Documentação CopilotKit](https://docs.copilotkit.ai/)
- [Documentação Next.js](https://nextjs.org/docs)
- [Documentação OpenRouter API](https://openrouter.ai/docs)
