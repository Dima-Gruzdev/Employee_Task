FROM python:3.11-slim AS builder

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV PATH=$POETRY_VENV/bin:$POETRY_HOME/bin:$PATH

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry

WORKDIR /app
COPY pyproject.toml poetry.lock ./


RUN poetry config virtualenvs.create false \
    && poetry install --only=main --no-dev --no-interaction --no-ansi

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH=/opt/poetry/bin:$PATH

WORKDIR /app


COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY . .


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]