FROM python:3.10-slim

# Impede o Python de gerar arquivos .pyc e envia os logs diretamente para o terminal (sem buffer)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências do sistema necessárias para compilar pacotes Python (ex: psycopg2, Pillow)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala as dependências do Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia os arquivos do projeto para o container
COPY . /app/

# Expõe a porta que o Django vai rodar
EXPOSE 8080

# Comando para iniciar o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
