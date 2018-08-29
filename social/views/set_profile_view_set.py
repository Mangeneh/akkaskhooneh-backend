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
        user.profile_picture = request.FILES['profile_picture']
        user.save()
        serializer = SetProfilePicSerializer(user)
        return Response(serializer.data)
