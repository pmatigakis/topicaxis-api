#!/bin/bash
set -e

cd /app

if [ "$1" = "run" ]; then
    exec gunicorn topicaxisapi.api.wsgi:app --bind 0.0.0.0 --workers 2 --worker-class uvicorn.workers.UvicornWorker --max-requests 200 --max-requests-jitter 20
elif [ "$1" = "migrate" ]; then
    export $(grep -v '^#' /app/.env | xargs)
    exec dockerize -template /app/alembic.ini.tmpl:/app/alembic.ini alembic upgrade head
fi

exec "$@"
