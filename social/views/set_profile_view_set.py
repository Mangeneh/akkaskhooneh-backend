from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import utils
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger('social')


class SetProfilePicViewSet(APIView):

    def post(self, request, format=None):
        ip = utils.get_client_ip(request)
        utils.start_method_log('SetProfilePicViewSet: post',
                               username=request.user.username,
                               ip=ip)
        if request.FILES.get('profile_picture'):
            try:
                utils.validate_image(request.FILES.get('profile_picture'))
            except ValidationError as e:
                data = {
                    "error": e
                }

                logger.info("SetProfilePicViewSet: post "
                    "(Profile picture is not valid) username:{}, ip: {}".format(
                        request.user.username, ip))

                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            user = request.user
            user.profile_picture = request.FILES.get('profile_picture')
            user.save()

            logger.info("SetProfilePicViewSet: post "
                    "(Profile picture successfully changed.) username:{}, ip: {}".format(
                        request.user.username, ip))

            return Response(data={}, status=status.HTTP_200_OK)
        else:
            data = {
                "error": ["Profile picture is required."]
            }
            logger.info("SetProfilePicViewSet: post "
                    "(Profile picture is required.) username:{}, ip: {}".format(
                        request.user.username, ip))
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
