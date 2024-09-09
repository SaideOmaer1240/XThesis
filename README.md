# XThesis

XThesis é uma plataforma desenvolvida em Django com React, Docker e PostgreSQL. Ela tem o objetivo de automatizar e otimizar a criação de teses acadêmicas.

## Requisitos

Certifique-se de ter as seguintes ferramentas instaladas em sua máquina antes de executar o projeto:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/) (Opcional, apenas se desejar rodar o front-end fora do Docker)

## Configuração do Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/SaideOmaer1240/XThesis.git 
 
 

### 2. Defina as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```bash
# .env

# Variáveis do Django
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Variáveis do banco de dados
POSTGRES_DB=xthesisdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432

# Outras variáveis de configuração
REDIS_URL=redis://redis:6379
```

### 3. Execute o Docker Compose

Construa e inicie os contêineres usando o Docker Compose:

```bash
docker-compose up --build
```

Este comando vai:
- Construir a imagem do back-end com Django e PostgreSQL.
- Construir a imagem do front-end com React.
- Subir um serviço Redis para o gerenciamento de canais.

### 4. Aplicar as migrações do banco de dados

Após subir o projeto, entre no contêiner do backend e aplique as migrações do banco de dados:

```bash
docker-compose exec backend python manage.py migrate
```

### 5. Acesse o projeto

Com todos os contêineres rodando, você pode acessar a aplicação nos seguintes endereços:

- Front-end: [http://localhost:3000](http://localhost:3000)
- Back-end (API): [http://localhost:8000](http://localhost:8000/admin)

## Comandos Úteis

### Parar os contêineres

```bash
docker-compose down
```

### Atualizar dependências do Python ou Node.js

Para atualizar as dependências do Python, entre no contêiner backend e instale as bibliotecas:

```bash
docker-compose exec backend pip install -r requirements.txt
```

Para atualizar as dependências do Node.js no frontend:

```bash
docker-compose exec frontend npm install
```

## Estrutura do Projeto

```bash
xthesis/
│
├── backend/                   # Backend do Django
│   ├── Dockerfile-backend      # Dockerfile do backend
│   ├── manage.py               # Arquivo de gerenciamento do Django
│   ├── requirements.txt        # Dependências do Python
│   └── ...                     # Outros arquivos do Django
│
├── frontend/                   # Frontend React
│   ├── Dockerfile-frontend      # Dockerfile do frontend
│   ├── package.json            # Dependências do Node.js
│   └── src/                    # Código fonte do React
│
├── docker-compose.yml          # Configurações do Docker Compose
└── .env                        # Arquivo de variáveis de ambiente
```
 
 