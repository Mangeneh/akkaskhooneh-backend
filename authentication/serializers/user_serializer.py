from rest_framework import serializers
from rest_framework.response import Response
from authentication.utils import get_simplejwt_tokens

from authentication.models import User
from rest_framework.serializers import Serializer
from django.contrib.auth.password_validation import validate_password

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
        username = validated_data.get("username")
        password = validated_data.get("password")
        email = validated_data.get("email")
        profile_picture = validated_data.get("profile_pic")

        user = User.objects.create(username=username, password="", email=email)

        user.set_password(password)
        user.fullname = validated_data.get("fullname")
        user.bio = validated_data.get("bio")
        user.phone_number = validated_data.get("phone_number")
        user.profile_picture = profile_picture

        user.save()

        tokens = get_simplejwt_tokens(user)

        data = {
            'refresh': tokens['refresh'],
            'access': tokens['access']
        }
        return data

class UserChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    repeat_password = serializers.CharField(required=True)

    def validate_password(self, value):
        validate_password(value)
        return value

