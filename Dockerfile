FROM python:3.13-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y curl build-essential libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala Poetry via script oficial
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

# Cria diretório da app
WORKDIR /app

# Copia arquivos do projeto
COPY pyproject.toml poetry.lock* ./

# Instala dependências do projeto SEM virtualenv (instala direto no sistema)
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-root

# Copia o resto da aplicação
COPY . .

# Expõe a porta
EXPOSE 8000

# Comando de start com gunicorn
CMD ["gunicorn", "-c", "app:app"]
