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

Crie um arquivo `.env` no core do backend com as seguintes variáveis:

```bash
# .env

# Variáveis do Django
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,seu_dominio.com,
GROQ_API_KEY=sua_chave
GROQ_MODEL_NAME = "llama3-70b-8192"
ALLOWED_HOSTS=http://localhost:5173, https://your-frontend-domain.com 

DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=postgres
DATABASE_USER=postgres
DATABASE_HOST=seu_host.io
DATABASE_PASSWORD=sua_palavra_passe
DATABASE_PORT=5432


JWT_ACCESS_TOKEN_LIFETIME=30
JWT_REFRESH_TOKEN_LIFETIME=1
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOW_CREDENTIALS=True
GEMINI_API_KEY=sua_chave 

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
Por padrão ao executar docker compose as migrações serão feitas. Caso não seja feitas as migrações, entre no contêiner do backend e aplique as migrações do banco de dados:

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
│   ├── requirements.txt         # Dependências do Python  
│   ├── app
│   ├── core/    
│   │    ├── .env                # Arquivo de variáveis de ambiente
│   │    ├── settings.py  
│   │    └── ...                # Outros arquivos python   
│   └── ...                     # Outros arquivos do Django
│
├── frontend/                   # Frontend React
│   ├── Dockerfile-frontend      # Dockerfile do frontend
│   ├── package.json            # Dependências do Node.js
│   └── src/                    # Código fonte do React
│
├── docker-compose.yml          # Configurações do Docker Compose   
```
 
  
### Iniciar Nginx em um servidor Linux
 
####  Instalar o Nginx (se ainda não instalado):
   No Ubuntu/Debian, use:
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

#### Iniciar o serviço Nginx:
   Após a instalação, você pode iniciar o serviço Nginx com o seguinte comando:
   ```bash
   sudo systemctl start nginx
   ```
#### Verificar o status do Nginx:
   Para garantir que o Nginx esteja rodando corretamente, verifique o status:
   ```bash
   sudo systemctl status nginx
   ```

#### Habilitar o Nginx para iniciar automaticamente ao inicializar: 
   Se você deseja que o Nginx seja iniciado automaticamente ao reiniciar o servidor, execute:
   ```bash
   sudo systemctl enable nginx
   ```

#### Acessar o servidor Nginx:
   Após iniciar o Nginx, você pode acessar o servidor através do endereço IP do seu servidor no navegador:
   ```
   http://<seu-endereco-ip> 
   ```

 ### 2. Iniciar Nginx em um contêiner Docker

Se você estiver rodando Nginx em um contêiner Docker, o processo é um pouco diferente. Você precisará de um `Dockerfile` ou usar diretamente a imagem do Nginx.

#### Usando Docker Compose:

Aqui está um exemplo de como iniciar Nginx com Docker Compose:

1. **Crie ou edite o arquivo `docker-compose.yml`:**

   ```yaml
   version: '3'
   services:
     nginx:
       image: nginx:latest
       ports:
         - "80:80"
         - "443:443"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf
         - ./html:/usr/share/nginx/html
       networks:
         - my_network

   networks:
     my_network:
       driver: bridge
   ```

2. **Iniciar o Nginx com Docker Compose:**

   Execute o seguinte comando na pasta onde está o `docker-compose.yml`:

   ```bash
   docker-compose up -d
   ```

   O `-d` rodará o Nginx em segundo plano (modo "detached").

3. **Verificar se o Nginx está rodando:**

   Verifique os contêineres ativos:
   ```bash
   docker ps
   ```

4. **Acessar o Nginx:**
   Agora, você pode acessar o Nginx em `http://localhost` ou `http://<seu-endereco-ip>`.

---

Se você estiver enfrentando algum erro específico ou precisar de mais detalhes sobre a configuração do Nginx em seu projeto, me avise!