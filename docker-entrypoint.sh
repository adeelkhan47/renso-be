#!/bin/sh

set -e
cd /app/
. .venv/bin/activate

cd src

while ! flask db upgrade
do
     echo "Retry..."
     sleep 1
done

#exec celery -A tasks.email worker -l INFO --pool=solo &
#exec celery -A tasks.email beat -l INFO &
#exec celery -A tasks.queue beat -l INFO &
exec gunicorn --bind 0.0.0.0:5000 --forwarded-allow-ips='*' wsgi:app
