import { NextApiRequest, NextApiResponse } from 'next';
import {
  CopilotRuntime,
  OpenAIAdapter,
  copilotRuntimeNextJSPagesRouterEndpoint,
} from '@copilotkit/runtime';
import OpenAI from 'openai';

/** 
const openai = new OpenAI({
  apiKey:
  "Ae9prhY892FmxazFQwX7rK2eauRvKUakIn7nah3nGPFkAhEyPESpJQQJ99BBACYeBjFXJ3w3AAABACOGIyML",
  baseURL: "https://otimizai-openai2.openai.azure.com/openai/deployments/gpt-4",
  defaultQuery: { "api-version": "2024-10-21" },
  defaultHeaders: {
    "api-key":
    "Ae9prhY892FmxazFQwX7rK2eauRvKUakIn7nah3nGPFkAhEyPESpJQQJ99BBACYeBjFXJ3w3AAABACOGIyML",
  },
});
*/

const openai = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: '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'
});

const serviceAdapter = new OpenAIAdapter({
  openai,
  model: 'gpt-4'
});

const handler = async (req: NextApiRequest, res: NextApiResponse) => {
  const runtime = new CopilotRuntime({
    remoteEndpoints: [ 
        { 
          url: "http://localhost:8001/copilotkit_remote",
        },
    ],
  });

  const handleRequest = copilotRuntimeNextJSPagesRouterEndpoint({
    endpoint: '/api/copilotkit',
    runtime,
    serviceAdapter,
  });

  try {
    return await handleRequest(req, res);
  } catch (error) {
    console.error('Error in copilotkit handler:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
};

export default handler;