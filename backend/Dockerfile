FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mcp_client.py .
COPY mcp_server.py .
COPY dev_server.py .

COPY gint_ingenst.py .
RUN pip install --no-cache-dir gitingest

COPY gitingest_server.py .

EXPOSE 8003
EXPOSE 8002
EXPOSE 8000

