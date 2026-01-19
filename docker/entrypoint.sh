#!/bin/sh

echo "Aguardando banco de dados..."
sleep 1

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
