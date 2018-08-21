from rest_framework import generics, permissions

from authentication.models import User
from authentication.serializers.user_serializer import UserSerializer

class register(generics.ListCreateAPIView):
    http_method_names = ['post']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
