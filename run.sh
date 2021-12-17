#!/bin/bash
python manage.py migrate
python manage.py migrate --database=game_db
python manage.py runserver 0.0.0.0:8000