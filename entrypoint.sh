#!/bin/sh
set -e

# Явно активируем виртуальное окружение
. /app/.venv/bin/activate

echo "Running Alembic migrations..."
uv run alembic upgrade head

echo "Starting Granian..."
exec granian --interface asgi --host 0.0.0.0 --port 8000 --workers 4 --loop uvloop app.main:app