FROM python:3.11-slim

# Instalar OPA
RUN apt-get update && apt-get install -y curl && \
    curl -L -o opa https://openpolicyagent.org/downloads/v0.58.0/opa_linux_amd64_static && \
    chmod 755 ./opa && \
    mv opa /usr/local/bin && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar usuário não-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expor porta
EXPOSE 8002

# Comando de inicialização
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
