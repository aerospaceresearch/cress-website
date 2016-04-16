#!/bin/bash
export DJANGO_SETTINGS_MODULE=cress.settings.production
export PYTHONUNBUFFERED=0
mkdir -p /home/uid1000/cress
mkdir -p /home/uid1000/cress/logs
mkdir -p /home/uid1000/cress/run
chmod -R 777 /home/uid1000/cress/run
python3 manage.py migrate
python3 manage.py collectstatic --noinput
exec uwsgi --http 0.0.0.0:8012 --wsgi-file /opt/code/cress/cress/wsgi.py --master --processes 10 --threads 3
