from .base import *

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.11.140']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# TODO Database connection in not configure.
# TODO Install 'libmysqlclient-dev' package before installing mysqlclient.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myproject',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
