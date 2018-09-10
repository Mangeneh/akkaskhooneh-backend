from rest_framework import views, status
from rest_framework.response import Response
from authentication.models import User
from social.models import Request, Followers
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import logging
import utils

logger = logging.getLogger('social')


class DeleteFollowRequest(views.APIView):

    def post(self, request):
        target_user_name = request.data.get('username')
        request_username = request.user.username

        ip = utils.get_client_ip(request)

        utils.start_method_log('DeleteFollowRequest: post',
                               authorized_user=request.user.username,
                               request_user=target_user_name)

        if target_user_name is None:
            logger.info('DeleteFollowRequest: post '
                        '(username is required) username:{}, ip: {}'.format(
                            request.user.username, ip))
            return Response(
                data={"error": "Username required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            target_user = User.objects.get(username=target_user_name)
        except ObjectDoesNotExist:
            logger.info('DeleteFollowRequest: post '
                        '(Username not found) username:{}, ip: {}'.format(
                            request.user.username, ip))
            return Response(
                data={"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            request = Request.objects.get(
                requester=request.user, requestee=target_user)
        except ObjectDoesNotExist:
            logger.info('DeleteFollowRequest: post '
                        '(You didnt request this user.) username:{}, ip: {}'.format(
                            request.user.username, ip))
            return Response(
                data={"error": "You didnt request this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        request.delete()
        logger.info('DeleteFollowRequest: post '
                    '(Follow request deleted succesfully) username:{}, ip: {}'.format(
                        request_username, ip))
        return Response(
            data={'details': 'Follow request deleted succesfully'},
            status=status.HTTP_200_OK
        )
