from rest_framework import serializers


class UserEditProfileSerializer(serializers.Serializer):
    bio = serializers.CharField(max_length=255, default=None, allow_blank=True)
    fullname = serializers.CharField(max_length=50, default=None, allow_blank=True)
