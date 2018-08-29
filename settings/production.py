from .base import *

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.11.140']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'testproject',
        'USER': 'root',
        'PASSWORD': 'nX2G7yeRgUf2dcR',
        'HOST': '172.17.0.4',
        'PORT': '',
    }
}

MEDIA_ROOT = '/mnt/nginx/media'
STATIC_ROOT = '/mnt/nginx/static'