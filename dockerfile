# Dockerfile para MindlyAI
FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema necessárias para Python e requests HTTP
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia o código-fonte
COPY . /app

EXPOSE 8000

# Inicia a API FastAPI com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]