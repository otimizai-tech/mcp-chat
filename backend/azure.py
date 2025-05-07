import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://otimizai-openai2.openai.azure.com/")
DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4")
API_VERSION = os.getenv("AZURE_API_VERSION", "2024-10-21")
API_KEY = os.getenv("AZURE_API_KEY", "")

if not API_KEY:
    raise ValueError("A chave da API do OpenAI no Azure não foi definida.")

__all__ = ['AZURE_OPENAI_ENDPOINT', 'DEPLOYMENT_NAME', 'API_VERSION', 'API_KEY']

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

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    result = response.json()
    print(json.dumps(result, indent=2, ensure_ascii=False))
else:
    print(f"Erro {response.status_code}: {response.text}")
