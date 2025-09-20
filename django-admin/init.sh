#!/bin/bash
set -e
python manage.py migrate
python manage.py create_superuser
python manage.py runserver 0.0.0.0:8000
uwsgi --strict --ini uwsgi/uwsgi.ini
