import re

from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        """
        Creates and saves a User with the given email, username and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        if not username:
            raise ValueError('The given username must be set')

        if not re.match("^[a-zA-Z0-9_]{4,20}", username):
            raise ValidationError('Your username is not valid')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password, **extra_fields):

        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)

        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, password, **extra_fields)
