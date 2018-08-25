from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from social.serializers.profile_serializer import ProfileSerializer


class ProfileViewSet(APIView):
    """
    Retrieve a profile instance.
    """

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username=None, format=None):
        if username is None:
            user = request.user
            serializer = ProfileSerializer(user)
            return Response(serializer.data)
        else:
            user = User.objects.filter(username=username).first()
            serializer = ProfileSerializer(user)
            return Response(serializer.data)
