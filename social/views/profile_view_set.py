from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from social.serializers.profile_serializer import ProfileSerializer


class ProfileViewSet(APIView):
    """
    Retrieve a profile instance.
    """

    def _response(self, data, request):
        if data['profile_picture']:
            data['profile_picture'] = str(request.scheme) + '://' + request.get_host() + data['profile_picture']
        return Response(data)

    def get(self, request, username=None, format=None):
        if username is None:
            user = request.user
            serializer = ProfileSerializer(user)
            data = serializer.data

            return self._response(data, request)
        else:
            user = User.objects.filter(username=username).first()

            if user is None:
                response_content = {"detail": "User not Found"}
                return Response(response_content, status.HTTP_404_NOT_FOUND)

            serializer = ProfileSerializer(user)

            data = serializer.data
            data.pop('email', None)

            return self._response(data, request)
