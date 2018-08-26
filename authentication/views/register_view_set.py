from rest_framework import generics, permissions, status, authentication
from rest_framework.response import Response
from authentication.models import User
from authentication.serializers.user_serializer import UserSerializer, UserChangePasswordSerializer, UserEditProfileSerializer, EmailSerializer
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist


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
        object = self.get_object()
        serializer = UserChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            password = serializer.data.get("password")
            repeat_password = serializer.data.get("repeat_password")

            if not object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)

            if password != repeat_password:
                return Response({"password": ["Password does not match."]},
                                status=status.HTTP_400_BAD_REQUEST)

            object.set_password(serializer.data.get("password"))
            object.save()
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditProfile(APIView):

    http_method_names = ['post']
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def post(self, request):
        object = self.get_object()
        serializer = UserEditProfileSerializer(data=request.data)
        if serializer.is_valid():
            bio = serializer.data.get("bio")
            fullname = serializer.data.get("fullname")
            if bio != None:
                object.bio = bio
            if fullname != None:
                object.fullname = fullname
            object.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CheckEmailApiView(APIView):
    """ This api view use for check email address exist in database."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = request.POST.get('email')
            try:
                User.objects.get(email=email)
            except ObjectDoesNotExist:
                return Response({
                    "message": "Email is does not exist."
                }, status=status.HTTP_200_OK)
            return Response({
                "message": "Email is exist"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "Email address is not valid"
            }, status=status.HTTP_400_BAD_REQUEST)
