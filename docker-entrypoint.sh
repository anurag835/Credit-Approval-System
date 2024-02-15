#!/bin/bash

sleep 2

echo "Apply database migrations"
python manage.py migrate

echo "Running Server"
python manage.py runserver 0.0.0.0:8000