from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
import utils
import logging

logger = logging.getLogger('authentication')


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        utils.start_method_log('UserChangePasswordSerializer: validate_new_password')

        validate_password(value)

        logger.info('UserChangePasswordSerializer: validate_new_password (password validated!)')

        return value
