#!/usr/bin/env bash

python manage.py collectstatic
python manage.py runserver 8000