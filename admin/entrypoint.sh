#!/bin/bash

until PGPASSWORD=$PG_PASSWD psql -h "$PG_HOST" -U "$PG_USER" -d "$PG_DBNAME" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up"

python3 manage.py migrate
python3 manage.py collectstatic --no-input

gunicorn -c gunicorn.conf.py config.wsgi:application
