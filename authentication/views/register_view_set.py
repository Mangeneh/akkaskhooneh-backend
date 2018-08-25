from rest_framework import generics, permissions, status
from rest_framework.response import Response
from authentication.models import User
from authentication.serializers.user_serializer import UserSerializer, UserChangePasswordSerializer
from rest_framework.views import APIView

class RegisterViewSet(generics.ListCreateAPIView):
    http_method_names = ['post']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

class ChangePassword(APIView):

    http_method_names = ['put']
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = UserChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            password = serializer.data.get("password")
            repeat_password = serializer.data.get("repeat_password")

            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)

            if password != repeat_password:
                return Response({"password": ["Password does not match."]},
                                status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("password"))
            self.object.save()
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)