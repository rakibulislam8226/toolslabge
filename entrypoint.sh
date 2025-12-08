#!/bin/sh
set -e

# Wait for Redis
echo "Waiting for Redis..."
until nc -z $REDIS_HOST $REDIS_PORT; do
  echo "Redis is unavailable - sleeping"
  sleep 1
done
echo "Redis is up!"

# Wait for Postgres
echo "Waiting for Postgres..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done
echo "Postgres is up!"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Execute main command
exec "$@"
