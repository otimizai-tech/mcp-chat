import os
import requests
import json

# Configuração do endpoint e credenciais
AZURE_OPENAI_ENDPOINT = "https://otimizai-openai2.openai.azure.com/"
DEPLOYMENT_NAME = "gpt-4"
API_VERSION = "2024-10-21"
API_KEY = "Ae9prhY892FmxazFQwX7rK2eauRvKUakIn7nah3nGPFkAhEyPESpJQQJ99BBACYeBjFXJ3w3AAABACOGIyML"

if not API_KEY:
    raise ValueError("A chave da API do OpenAI no Azure não foi definida.")

# Export these variables
__all__ = ['AZURE_OPENAI_ENDPOINT', 'DEPLOYMENT_NAME', 'API_VERSION', 'API_KEY']

# URL do endpoint
url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version={API_VERSION}"

# Payload da requisição
payload = {
    "messages": [
        {"role": "system", "content": "Você é um assistente de IA."},
        {"role": "user", "content": "Quero saber exatamente qual modelo você é?"}
    ],
    "max_tokens": 800,
    "temperature": 0.7,
    "top_p": 0.95
}

# Cabeçalhos corrigidos
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY  # Alterado para "api-key"
}

# Enviando a requisição
response = requests.post(url, headers=headers, json=payload)

# Verificando a resposta
if response.status_code == 200:
    result = response.json()
    print(json.dumps(result, indent=2, ensure_ascii=False))
else:
    print(f"Erro {response.status_code}: {response.text}")
