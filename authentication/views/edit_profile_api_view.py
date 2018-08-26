from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import UserEditProfileSerializer


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
            if bio is not None:
                object.bio = bio
            if fullname is not None:
                object.fullname = fullname
            object.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
