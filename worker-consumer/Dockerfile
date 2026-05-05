FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME="/opt/poetry"
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN poetry config virtualenvs.create false

WORKDIR /app

COPY worker-consumer/pyproject.toml worker-consumer/poetry.lock ./
RUN poetry install --no-interaction --no-ansi --no-root

COPY shared ./shared
COPY worker-consumer/worker ./worker

ENV PYTHONPATH="/app"

WORKDIR /app/worker
