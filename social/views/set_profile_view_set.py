from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import utils
from social.serializers.set_profile_serializer import SetProfilePicSerializer


class SetProfilePicViewSet(APIView):

    def post(self, request, format=None):
        ip = utils.get_client_ip(request)
        utils.start_method_log('SetProfilePicViewSet: post',
                               username=request.user.username,
                               ip=ip)

        user = request.user
        user.profile_picture = request.FILES.get('profile_picture')
        if not user.profile_picture:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'details': 'Your picture is not uploaded'})
        user.save()
        serializer = SetProfilePicSerializer(user)
        return Response(serializer.data)
