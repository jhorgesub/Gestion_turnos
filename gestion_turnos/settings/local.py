

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []





# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
<<<<<<< HEAD
        'NAME': 'dbgestionturnos',
=======
        'NAME': 'turnos',
>>>>>>> d86f66e2a6c9b02b5031c797de452e0739e3fdd6
        'USER': 'postgres',
        'PASSWORD': '0314092',
        'HOST':'localhost',
        'PORT':'5432'
    }
}

""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + 'db.sqlite3',
    }
} """



EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER='info.app.g6@gmail.com' ## Es un correo creado para enviar las solicitudes de cambo de pass
EMAIL_HOST_PASSWORD='informatorio2020'