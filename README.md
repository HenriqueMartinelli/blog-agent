# 🧠 Blog Agent – Agente Autônomo de Criação de Conteúdo

Este projeto é um agente autônomo de geração de posts de blog, construído em Python com FastAPI, integrando IA (OpenAI GPT) para gerar conteúdo original com base em temas populares extraídos de fontes externas como Reddit.

---

## 🏗️ Arquitetura Utilizada

A estrutura do projeto segue uma arquitetura modular inspirada em **Clean Architecture**, com camadas bem definidas que separam responsabilidades de forma clara:

```
├── routers/         # Rotas da API
├── controllers/     # Orquestração do fluxo de cada endpoint
├── services/        # Lógica de negócio (ex: geração de conteúdo, temas, IA)
├── repositories/    # Persistência e acesso a dados (PostgreSQL)
├── models/          # Models SQLAlchemy
├── schemas/         # Schemas Pydantic (entrada/saída)
├── protocols/       # Contratos de serviço via typing.Protocol
├── middlewares/     # Logging, tratamento de erros
├── core/            # Configurações globais (ex: settings, .env)
├── utils/           # Funções auxiliares (ex: logging setup)
└── test/            # Testes unitários e de integração
```

## 🧩 Padrões de Projeto Utilizados

- **Service Layer Pattern** – Encapsula regras de negócio isoladamente
- **Repository Pattern** – Abstrai acesso ao banco, separando persistência
- **Dependency Injection** – Services e repos recebem dependências externas
- **Protocol (Interface Segregation)** – Contratos desacoplados para facilitar testes
- **Retry Pattern** – Pode ser adicionado com tenacity para dar resiliência a chamadas externas

---

## 🛢️ Escolha por PostgreSQL em vez de MongoDB

O projeto foi implementado com **PostgreSQL** por três razões principais:

1. **Natureza relacional dos dados** – Posts possuem estrutura fixa com campos bem definidos.
2. **Necessidade de integridade transacional** – Operações como criação de post exigem consistência.
3. **Simplicidade e robustez para o escopo atual** – MongoDB seria mais indicado em cenários com dados semi-estruturados, como logs, histórico de prompts ou documentos dinâmicos.

---

## 🐳 Execução com Docker Compose

1. Certifique-se de ter Docker e Docker Compose instalados.
2. Execute o projeto com:

```bash
docker-compose up --build
```

3. Acesse a aplicação em: [http://localhost:8000](http://localhost:8000)

Para parar os contêineres:

```bash
docker-compose down
```

---

## 📄 Variáveis de Ambiente (.env)

Antes de rodar a aplicação, crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
# 🤖 OpenAI
OPENAI_API_KEY="KEY OPENIA"
OPENAI_MODEL="gpt-3.5-turbo" - Model

# 💾 Banco
DATABASE_URL=postgresql+asyncpg://blog_user:senha123@blog_postgres:5432/blog_db

# ⚙️ Ambiente
DEV=true
ENVIRONMENT=development
```


---

## 🤖 Geração Autônoma de Conteúdo

A rota `POST /posts/autonomous` é responsável por criar automaticamente um post de blog. Esse processo acontece de forma autônoma, integrando duas etapas principais:

1. **Extração de Tópico**: O agente identifica um assunto popular em uma comunidade do Reddit, definida via payload. Por exemplo:
   ```json
   {
     "subreddit": "programming"
   }
   ```

Essa automação permite que o projeto produza conteúdo relevante e atualizado com mínima intervenção humana, sendo ideal para blogs que desejam manter uma publicação constante baseada em tendências do momento.

## 📚 Documentação da API

Após subir o projeto, você pode acessar a documentação interativa gerada automaticamente pelo **FastAPI** nos seguintes endpoints:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

Essas interfaces permitem testar os endpoints diretamente pelo navegador e visualizar os contratos da API com base nos `schemas` definidos.
