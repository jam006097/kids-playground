from .base import *

DEBUG = False
ALLOWED_HOSTS = ["jam006097.pythonanywhere.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "jam006097$kids",
        "USER": "jam006097",
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": "jam006097.mysql.pythonanywhere-services.com",
        "PORT": "3306",
    }
}
