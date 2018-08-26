from rest_framework import serializers
from authentication.models import User


class SetProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'profile_picture')
