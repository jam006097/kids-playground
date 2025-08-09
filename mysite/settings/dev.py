from .base import *
import os
import sys

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# ローカルでの手動テスト時のみ実際にメールを送信する
if "runserver" in sys.argv:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
else:
    # テスト実行時はコンソールに出力
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
