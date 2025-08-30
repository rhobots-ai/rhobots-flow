#!/bin/bash
set -e

if [ "$1" = "web" ]; then
  echo "🔄 Running Django migrations..."
  python manage.py migrate --noinput

  echo "🚀 Starting Daphne (ASGI)..."
  exec daphne -b 0.0.0.0 -p 8000 config.asgi:application
elif [ "$1" = "dev" ]; then
    echo "🔄 Running Django migrations..."
    python manage.py migrate --noinput

    echo "🚀 Starting Daphne (ASGI) dev server..."
    exec daphne -b 0.0.0.0 -p 8000 config.asgi:application
elif [ "$1" = "celery" ]; then
  echo "📦 Starting Celery worker..."
  exec celery -A config worker --loglevel=INFO
elif [ "$1" = "beat" ]; then
  echo "⏰ Starting Celery beat..."
  exec celery -A config beat --loglevel=INFO
else
  echo "❓ Unknown command: $1"
  exec "$@"
fi
