from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import serializers

from authentication.utils import get_simplejwt_tokens
from authentication.models import User
import utils
import logging

logger = logging.getLogger('authentication')


class UserSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField(max_length=254, read_only=True)
    access = serializers.CharField(max_length=254, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password',
                  'fullname', 'bio', 'phone_number',
                  'refresh', 'access',)
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'write_only': True},
                        'username': {'write_only': True},
                        'phone_number': {'write_only': True},
                        'fullname': {'write_only': True},
                        'bio': {'write_only': True},
                        }

    def create(self, validated_data):

        log_data = validated_data.copy()

        log_data.pop('password', None)

        utils.start_method_log('UserSerializer: create', **log_data)

        username = validated_data.get("username")
        password = validated_data.get("password")
        email = validated_data.get("email")

        user = User.objects.create_user(username=username, password=password, email=email)

        user.fullname = validated_data.get("fullname")
        user.bio = validated_data.get("bio")
        user.phone_number = validated_data.get("phone_number")

        user.save()

        tokens = get_simplejwt_tokens(user)

        data = {
            'refresh': tokens['refresh'],
            'access': tokens['access']
        }
        return data

    def validate(self, data):
        log_data = data.copy()
        log_data.pop('password', None)
        utils.start_method_log('UserSerializer: validate', **log_data)

        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(**data)
        # get the password from the data
        password = data.get('password')
        username = data.get("username")

        errors = {}
        try:
            # validate the password and catch the exception
            validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except ValidationError as e:
            logger.info('UserSerializer: validate (username: {}: password not validated!)'.format(username))
            errors['password'] = list(e.messages)
        try:
            User.objects.check_username(username=username)
        except ValidationError as e:
            logger.info('UserSerializer: validate (username {} not validated!)'.format(username))
            errors['username'] = e.message
        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)
