# Usar a imagem oficial do Python 3.10
FROM python:3.10-slim

# Instalar pacotes de sistema necessários para compilar bibliotecas de IA
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Definir a pasta de trabalho
WORKDIR /app

# Copiar apenas os requisitos primeiro
COPY requirements.txt .

# Atualizar o instalador e instalar as bibliotecas
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar todo o código fonte (ignorando o que está no .dockerignore)
COPY . .

# Expor a porta 8000
EXPOSE 8000

# Rodar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]