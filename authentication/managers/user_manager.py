import re
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
import utils
import logging

logger = logging.getLogger('authentication')


class UserManager(BaseUserManager):
    use_in_migrations = True

    def check_username(self, username):
        """
        Checks can create a User with given info
        """
        utils.start_method_log('UserManager: check_username', username=username)

        if not username:
            logger.info('UserManager: check_username (The given username must be set)')
            raise ValidationError('The given username must be set')

        if not re.match("^[a-zA-Z0-9_]{4,20}$", username):
            logger.info('UserManager: check_username (Your username is not valid)')
            raise ValidationError('Your username is not valid')

    def _create_user(self, email, username, password, **extra_fields):
        """
        Creates and saves a User with the given email, username and password.
        """
        utils.start_method_log('UserManager: _create_user', email=email, username=username, **extra_fields)

        if not email:
            logger.info('UserManager: _create_user (The given email must be set)')
            raise ValueError('The given email must be set')

        if not username:
            logger.info('UserManager: _create_user (The given username must be set)')
            raise ValueError('The given username must be set')

        if not re.match("^[a-zA-Z0-9_]{4,20}$", username):
            logger.info('UserManager: _create_user (Your username is not valid)')
            raise ValidationError('Your username is not valid')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        logger.info('UserManager: _create_user (user created email: {}, username: {})'.format(email, username))

        return user

    def create_user(self, email, username, password, **extra_fields):

        utils.start_method_log('UserManager: create_user', email=email, username=username, **extra_fields)

        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)

        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):

        utils.start_method_log('UserManager: create_superuser', email=email, username=username, **extra_fields)

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            logger.info('UserManager: create_superuser: Superuser must have is_superuser=True.')
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, password, **extra_fields)
