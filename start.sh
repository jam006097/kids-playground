#!/bin/bash

# データベースのマイグレーションを実行
/usr/local/bin/python manage.py migrate

# Gunicornを起動
/usr/local/bin/python -m gunicorn --bind 0.0.0.0:$PORT mysite.wsgi:application
