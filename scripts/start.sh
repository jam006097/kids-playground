#!/bin/bash

# データベースのマイグレーションを実行
/usr/local/bin/python3 manage.py migrate

# Gunicornを起動
/usr/local/bin/python3 -m gunicorn --bind 0.0.0.0:$PORT mysite.wsgi:application
