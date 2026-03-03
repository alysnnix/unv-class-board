# Class Board

Este projeto é uma aplicação Django com PostgreSQL focado na **gestão operacional escolar diária**, servindo como um "Painel Interativo" para secretarias e coordenadores.

O sistema permite gerenciar horários, alocação de professores e controle de faltas/substituições de forma centralizada e ágil.

## Módulos do Sistema (Apps)

O projeto é dividido em 4 módulos principais:

- **Home:** A base do sistema. Serve para cadastrar a infraestrutura da escola: Segmentos (ex: Ensino Fundamental, Médio), Períodos (Manhã, Tarde), Turmas, Professores e as disciplinas (Componentes Curriculares) que eles lecionam.
- **Grade:** Onde a organização do agendamento acontece. Ele cruza as Turmas com os Professores e os dias da semana para montar a "Grade" (o quadro de horários).
- **Ocorrência:** O módulo de "gestão de crises". Se um professor falta (`Professor_Ausente`), a secretaria registra o motivo (`Justificativa`) e já aloca um substituto (`Professor_Substituto`) para cobrir a grade.
- **Mensagem:** Um sistema de comunicação em massa. Permite criar comunicados categorizados (Eventos, Pedagógicos, Administrativos) e direcioná-los para turmas ou professores específicos.

## Funcionalidades e Fluxos

A interface do usuário é construída quase totalmente como uma ferramenta de Back-Office (uso interno) utilizando o tema dinâmico **Django Jazzmin** para o Painel Administrativo. As principais funcionalidades incluem:

1. **Gestão via Admin:** Toda a operação (cadastros, montagem de grade, registro de ocorrências) é feita através de uma interface administrativa bonita e responsiva configurada em `config/settings.py`.
2. **Geração de Relatórios (PDF):** Integração com a biblioteca `ReportLab` que permite exportar listas e registros selecionados no painel diretamente para formato PDF, prontos para impressão.
3. **Dashboards Visuais:** O projeto conta com a rota `/chart/` (integrada via `django-chartjs`) preparada para exibir gráficos estatísticos com os dados da escola.

---

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