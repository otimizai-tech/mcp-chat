FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mcp_client.py .
COPY mcp_server.py .
COPY dev_server.py .

EXPOSE 8002
EXPOSE 8000

