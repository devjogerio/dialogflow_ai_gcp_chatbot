# Usa uma imagem base oficial do Python leve (Slim) para reduzir o tamanho do container
FROM python:3.10-slim

# Define variáveis de ambiente para otimizar o Python em containers
# PYTHONDONTWRITEBYTECODE: Impede que o Python escreva arquivos .pyc no disco
ENV PYTHONDONTWRITEBYTECODE 1
# PYTHONUNBUFFERED: Garante que os logs sejam enviados diretamente para o console (essencial para Cloud Logging)
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias para compilar pacotes Python (ex: psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos para o container
COPY requirements.txt /app/

# Instala as dependências Python listadas
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código fonte do projeto para o diretório de trabalho
COPY . /app/

# Expõe a porta 8080 (documentação para quem roda o container)
EXPOSE 8080

# Define a variável de ambiente PORT com valor padrão 8080 (caso não seja injetada)
ENV PORT 8080

# Comando para iniciar a aplicação usando Gunicorn
# nexus_admin.wsgi: aponta para o arquivo WSGI do projeto Django
# --bind 0.0.0.0:8080: escuta em todas as interfaces na porta 8080
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 nexus_admin.wsgi:application
