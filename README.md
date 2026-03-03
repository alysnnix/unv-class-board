# Class Board

Este projeto é uma aplicação Django com PostgreSQL para gerenciamento escolar. 

## Requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Como rodar o projeto com Docker (Recomendado)

A forma mais fácil de rodar o projeto sem precisar configurar nada localmente na sua máquina é utilizando o Docker Compose. Ele subirá automaticamente o Banco de Dados e a Aplicação em contêineres separados e conectados.

### 1. Inicie o projeto

No terminal, dentro da pasta raiz do projeto, execute o comando:

```bash
docker-compose up -d --build
```

- Este comando vai baixar as imagens necessárias, construir o contêiner do Django instalando todas as dependências do `requirements.txt`, iniciar o banco de dados e rodar o servidor na porta **8080**.

### 2. Execute as migrações

Para garantir que a estrutura do banco de dados está atualizada:

```bash
docker-compose exec web python manage.py migrate
```

### 3. Crie um usuário Administrador

Você vai precisar de um usuário para acessar o painel administrativo. Crie-o executando o comando abaixo e siga as instruções na tela:

```bash
docker-compose exec web python manage.py createsuperuser
```

### 4. Acesse o sistema

Abra o seu navegador e acesse:

[http://localhost:8080/class-board/](http://localhost:8080/class-board/)

- Faça login com o usuário e a senha que você acabou de criar.

---

## Comandos Úteis (Docker)

- **Parar o projeto:** `docker-compose down`
- **Ver os logs da aplicação:** `docker-compose logs -f web`
- **Acessar o terminal do contêiner Django:** `docker-compose exec web /bin/bash`
- **Criar novas migrações:** `docker-compose exec web python manage.py makemigrations`

---

## Como rodar o projeto Localmente (Sem Docker para a Aplicação)

Se preferir rodar a aplicação localmente e apenas o banco no Docker, siga estes passos:

1. **Suba apenas o banco de dados via Docker:** 
   ```bash
   docker-compose up -d db
   ```
2. **Ative sua venv:** 
   ```bash
   source .venv/bin/activate
   ```
3. **Instale as dependências:** 
   ```bash
   pip install -r requirements.txt
   ```
4. **Execute as migrações:** 
   ```bash
   python manage.py migrate
   ```
5. **Rode o servidor:** 
   ```bash
   python manage.py runserver 8080
   ```
