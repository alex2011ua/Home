#!/bin/bash
python3 manage.py migrate
gunicorn AlexUA_Home.wsgi:application --bind "0.0.0.0:8000"


