from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from social.serializers.profile_serializer import ProfileSerializer


class ProfileViewSet(APIView):
    """
    Retrieve a profile instance.
    """

    def get(self, request, username=None, format=None):
        if username is None:
            user = request.user
            serializer = ProfileSerializer(user)
            return Response(serializer.data)
        else:
            user = User.objects.filter(username=username).first()

            if user is None:
                response_content = {"detail": "User not Found"}
                return Response(response_content, status.HTTP_404_NOT_FOUND)

            serializer = ProfileSerializer(user)
            return Response(serializer.data)
