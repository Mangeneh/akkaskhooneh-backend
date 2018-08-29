from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from authentication.serializers import EmailSerializer
import utils
import logging

logger = logging.getLogger('authentication')


class CheckEmailApiView(APIView):
    """ This api view use for check email address exist in database."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        ip = utils.get_client_ip(request)

        utils.start_method_log('CheckEmailApiView: post', ip=ip)

        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data['email']
            try:
                User.objects.get(email=email)
            except ObjectDoesNotExist:

                logger.info('CheckEmailApiView: post (Email does not exist. ip: {})'.format(ip))

                return Response({
                    "message": "Email does not exist."
                }, status=status.HTTP_200_OK)

            logger.info('CheckEmailApiView: post (Email exists. ip: {})'.format(ip))

            return Response({
                "message": "Email exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:

            logger.info('CheckEmailApiView: post (Email address is not valid. ip: {})'.format(ip))

            return Response({
                "message": "Email address is not valid"
            }, status=status.HTTP_400_BAD_REQUEST)
