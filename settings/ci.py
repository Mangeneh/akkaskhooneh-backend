from .base import *

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'backend',
        'USER': 'root',
        'PASSWORD': 'gkjfsda875afsd87',
        'HOST': 'mysql',
        'PORT': '',
    }
}
