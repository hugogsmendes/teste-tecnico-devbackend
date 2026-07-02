# Teste Tecnico Dev Backend

API REST para gerenciamento de tarefas desenvolvida com FastAPI, SQLAlchemy e PostgreSQL.

## Visão geral

O projeto expõe uma API com autenticação por login e operações de CRUD para tarefas. A aplicação usa cookie com token JWT para manter a sessão autenticada e inclui migrations com Alembic para evolução do banco de dados.

## Stack

- Python 3.12
- FastAPI
- SQLAlchemy 2
- Alembic
- PostgreSQL
- Docker e Docker Compose

## Boas práticas e organização

O projeto segue uma arquitetura simples em camadas para manter o código fácil de ler, testar e evoluir:

- `routes`: recebem a requisição HTTP, validam os dados de entrada e expõem os endpoints.
- `service`: concentra as regras de negócio e o fluxo principal de cada operação.
- `repository`: fala com o banco de dados e isola o acesso aos dados.
- `utils/dependencies.py`: centraliza a injeção de dependências do FastAPI, conectando sessão, repositório e serviço.
- `utils/auth.py`: concentra a autenticação, lendo o cookie `auth` no navegador em `get_current_user` e validando o token JWT antes de liberar o acesso às rotas protegidas.

Na prática, a rota chama o service, o service decide o que fazer e o repository executa a operação no banco. Para as rotas protegidas, o FastAPI usa `get_current_user` como dependência para checar o cookie `auth`, validar o JWT e confirmar se o usuário está autenticado antes de processar a requisição.

## Requisitos

- Python 3.12 ou superior
- Docker e Docker Compose
- Um ambiente com suporte a arquivos `.env`

## Arquivo de ambiente

Antes de subir a aplicação, crie um arquivo `.env` na raiz do projeto e copie as variáveis do arquivo `.env.example`.

### Criar o `.env`

- Linux:

```bash
cp .env.example .env
```

- Windows no Prompt de Comando:

```bat
copy .env.example .env
```

- Windows no PowerShell:

```powershell
Copy-Item .env.example .env
```

## Como executar no Linux


1. Suba os containers:

```bash
docker compose up -d
```

2. Execute as migrations:

```bash
docker compose exec api alembic upgrade head
```

3. Crie o usuário de teste:

```bash
python -m scripts.create_user
```

4. Acesse a documentação da API:

```text
http://localhost:8000/docs
```

5. No Swagger, faça login com as credenciais de teste antes de seguir com os testes das rotas protegidas.

## Como executar no Windows


1. Suba os containers no PowerShell ou no Prompt de Comando:

```powershell
docker compose up -d
```

2. Execute as migrations:

```powershell
docker compose exec api alembic upgrade head
```

3. Crie o usuário de teste:

```powershell
python -m scripts.create_user
```

4. Acesse a documentação da API:

```text
http://localhost:8000/docs
```

5. No Swagger, faça login com as credenciais de teste antes de seguir com os testes das rotas protegidas.

## Usuário de teste

O script cria um usuário inicial no banco com as credenciais abaixo:

- E-mail: `usuario@teste.com`
- Senha: `usuario123`

Use essas credenciais para se autenticar no Swagger antes de testar as rotas protegidas.

## Documentação das rotas

### `GET /health`

Request:

- Não recebe parâmetros.

Response:

- `200 OK`
- Body: `{"detail": "API is running"}`

### `POST /auth/login`

Request:

- Content-Type: `application/x-www-form-urlencoded`
- Campos enviados:
	- `username`
	- `password`

Response:

- `204 No Content`
- Define o cookie `auth` com o token JWT

Possíveis retornos de erro:

- `401 Unauthorized` com `{"detail": "Credencias inválidas"}`
- `500 Internal Server Error` com `{"detail": "Erro interno"}`

### `POST /tasks`

Autenticação:

- Exige cookie `auth`

Request:

- Body JSON com:
	- `titulo`
	- `descricao`
	- `status`

Exemplo:

```json
{
	"titulo": "Estudar FastAPI",
	"descricao": "Revisar rotas e schemas",
	"status": "Pendente"
}
```

Response:

- `201 Created`
- Body: `ResponseTarefa`

Exemplo:

```json
{
	"id": 1,
	"titulo": "Estudar FastAPI",
	"descricao": "Revisar rotas e schemas",
	"status": "Pendente",
	"data_de_criacao": "2026-07-01T12:00:00"
}
```

Possíveis retornos de erro:

- `401 Unauthorized` com `{"detail": "Não autenticado"}`
- `422 Unprocessable Entity` quando o campo `status` não corresponde a um valor permitido
- `500 Internal Server Error` com `{"detail": "Erro interno"}`

### `GET /tasks`

Autenticação:

- Exige cookie `auth`

Request:

- Query params opcionais:
	- `status_tarefa`
	- `titulo_tarefa`
	- `limit` (padrão: `5`, mínimo: `1`, máximo: `20`)
	- `offset` (padrão: `0`, mínimo: `0`)

Response:

- `200 OK`
- Body: lista de `ResponseTarefa`

Exemplo:

```json
[
	{
		"id": 1,
		"titulo": "Estudar FastAPI",
		"descricao": "Revisar rotas e schemas",
		"status": "Pendente",
		"data_de_criacao": "2026-07-01T12:00:00"
	},
	{
		"id": 2,
		"titulo": "Revisar migrations",
		"descricao": "Validar o fluxo com Alembic",
		"status": "Em andamento",
		"data_de_criacao": "2026-07-01T13:00:00"
	}
]
```

Possíveis retornos de erro:

- `401 Unauthorized` com `{"detail": "Não autenticado"}`
- `500 Internal Server Error` com `{"detail": "Erro interno"}`

### `GET /tasks/{id}`

Autenticação:

- Exige cookie `auth`

Request:

- Parâmetro de rota:
	- `id` como inteiro, referente ao ID da tarefa

Response:

- `200 OK`
- Body: `ResponseTarefa`

Exemplo:

```json
{
	"id": 1,
	"titulo": "Estudar FastAPI",
	"descricao": "Revisar rotas e schemas",
	"status": "Pendente",
	"data_de_criacao": "2026-07-01T12:00:00"
}
```

Possíveis retornos de erro:

- `401 Unauthorized` com `{"detail": "Não autenticado"}`
- `404 Not Found` com `{"detail": "Tarefa não encontrada"}`
- `500 Internal Server Error` com `{"detail": "Erro interno"}`

### `PATCH /tasks/{id}`

Autenticação:

- Exige cookie `auth`

Request:

- Parâmetro de rota:
	- `id` como inteiro, referente ao ID da tarefa
- Body JSON com campos opcionais:
	- `titulo`
	- `descricao`
	- `status`

Exemplo:

```json
{
	"status": "Em andamento"
}
```

Response:

- `204 No Content`

Possíveis retornos de erro:

- `401 Unauthorized` com `{"detail": "Não autenticado"}`
- `404 Not Found` com `{"detail": "Tarefa não encontrada"}`
- `422 Unprocessable Entity` quando o campo `status` não corresponde a um valor permitido
- `500 Internal Server Error` com `{"detail": "Erro interno"}`

### `DELETE /tasks/{id}`

Autenticação:

- Exige cookie `auth`

Request:

- Parâmetro de rota:
	- `id` como inteiro, referente ao ID da tarefa

Response:

- `204 No Content`
- Realiza o soft delete no Banco de Dados

Possíveis retornos de erro:

- `401 Unauthorized` com `{"detail": "Não autenticado"}`
- `404 Not Found` com `{"detail": "Tarefa não encontrada"}`
- `500 Internal Server Error` com `{"detail": "Erro interno"}`

### Modelos usados nas respostas

- `ResponseTarefa`:

```json
{
	"id": 1,
	"titulo": "Texto",
	"descricao": "Texto",
	"status": "Pendente",
	"data_de_criacao": "2026-07-01T12:00:00"
}
```

### Valores aceitos para status

- `Pendente`
- `Em andamento`
- `Concluída`

## Documentação interativa

Com a aplicação em execução, acesse:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
