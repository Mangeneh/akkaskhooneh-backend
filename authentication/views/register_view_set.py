from rest_framework import generics, permissions
from rest_framework.response import Response

from authentication.models import User
from authentication.serializers.user_serializer import UserSerializer


class RegisterViewSet(generics.ListCreateAPIView):
    http_method_names = ['post']
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
