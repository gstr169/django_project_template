#!/bin/bash
python utils/db_waiting.py &&
python manage.py migrate

python manage.py collectstatic --no-input &&
gunicorn -c gunicorn.py configs.wsgi
