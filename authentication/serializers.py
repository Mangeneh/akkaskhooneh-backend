from rest_framework import serializers
from authentication.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'fullname', 'bio', 'phone_number', 'register_date')
        extra_kwargs = {'password': {'write-only': True}}

    def create(self, validated_data):
        #TODO

        pass
