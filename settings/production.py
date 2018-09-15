from .base import *

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.11.140']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DJANGO_DB_NAME'),
        'USER': os.environ.get('DJANGO_DB_USER'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD'),
        'HOST': '172.17.0.4',
        'PORT': '',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

MEDIA_ROOT = '/mnt/nginx/media'
STATIC_ROOT = '/mnt/nginx/static'
