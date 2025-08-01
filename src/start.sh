#!/bin/bash

# Load environment variables from .env if it exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Collect static files
python manage.py collectstatic --noinput

# Run Gunicorn server
exec gunicorn automax.wsgi:application --bind 0.0.0.0:${PORT:-8080}
