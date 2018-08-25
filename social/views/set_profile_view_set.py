from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from social.serializers.profile_serializer import ProfileSerializer
from social.serializers.set_profile_serializer import SetProfilePicSerializer


class SetProfilePicViewSet(APIView):

    def post(self, request, format=None):
        user = request.user
        user.profile_picture = request.FILES['profile_picture']
        user.save()
        serializer = SetProfilePicSerializer(user)
        return Response(serializer.data)
