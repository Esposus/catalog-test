FROM python:3.14.4-alpine3.23
RUN apk update && \
    apk upgrade --no-cache && \
    apk add --no-cache libev-dev build-base curl && \
    rm -rf /var/cache/apk/*

# Установка uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app


COPY ./pyproject.toml ./uv.lock* ./


RUN uv venv && \
    . .venv/bin/activate && \
    uv sync --no-cache


COPY . /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PATH="/app/.venv/bin:${PATH}"
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
