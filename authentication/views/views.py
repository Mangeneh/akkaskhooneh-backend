from rest_framework import mixins, generics, status, viewsets, permissions

from authentication.models import User
from authentication.serializers import UserSerializer

class register(generics.ListCreateAPIView):
    http_method_names = ['post']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
