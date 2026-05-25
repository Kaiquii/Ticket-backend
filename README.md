# Ticket Backend

API para abertura e acompanhamento de tickets/chamados, criada com FastAPI, PostgreSQL e autenticação JWT.

## Tecnologias

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT
- Pytest
- Docker

## Funcionalidades

- Cadastro de usuario
- Login com token JWT
- Listagem de usuarios autenticada
- Criacao de tickets
- Listagem de tickets do usuario logado
- Atualizacao de status do ticket
- Exclusao de tickets
- Prioridade de tickets

## Variaveis de ambiente

Crie um arquivo `.env` baseado no `.env.example`. O `.env.example` deve ir para o GitHub como modelo, mas o `.env` real deve ficar apenas localmente e nao deve ser versionado.

```env
DATABASE_URL=postgresql+psycopg://postgres:4343@localhost:5432/ticket_db
JWT_SECRET_KEY=change-this-secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=4320
```

A senha de usuario deve ter no minimo 3 caracteres.

## Como executar localmente

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Crie o banco PostgreSQL:

```sql
CREATE DATABASE ticket_db;
```

Execute a API:

```bash
uvicorn app.main:app --reload
```

O comando acima aponta diretamente para o arquivo principal da aplicacao:

```text
app/main.py
```

Dentro dele existe a variavel `app`, que e a instancia do FastAPI carregada pelo Uvicorn. Por isso usamos `app.main:app`: o primeiro `app` e a pasta do projeto, `main` e o arquivo `main.py`, e o ultimo `app` e a variavel FastAPI.

A documentacao interativa ficara disponivel em:

```text
http://127.0.0.1:8000/docs
```

## Como executar com Docker

Suba a API e o PostgreSQL:

```bash
docker compose up --build
```

A API ficara disponivel em:

```text
http://127.0.0.1:8000
```

## Como rodar os testes

```bash
pytest
```

## Rotas

### Auth

```text
POST /auth/register
POST /auth/login
GET  /auth/users
```

### Tickets

As rotas de tickets exigem token JWT no header `Authorization: Bearer <token>`.

```text
POST  /tickets
GET   /tickets
PATCH /tickets/{ticket_id}/status
DELETE /tickets/{ticket_id}
```

Status permitidos:

```text
ABERTO
EM_ANDAMENTO
FINALIZADO
```

Prioridades permitidas:

```text
BAIXA
MEDIA
ALTA
```

## Exemplos de payload

### Cadastro

```json
{
  "name": "Kaique",
  "email": "kaique@email.com",
  "password": "4343"
}
```

### Login

```json
{
  "email": "kaique@email.com",
  "password": "4343"
}
```

### Criar ticket

```json
{
  "title": "Erro ao acessar sistema",
  "description": "Usuario nao consegue acessar a conta",
  "priority": "ALTA"
}
```

### Atualizar status

```json
{
  "status": "EM_ANDAMENTO"
}
```
