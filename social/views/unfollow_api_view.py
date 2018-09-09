from rest_framework import views, status
from rest_framework.response import Response

from social.models import Followers
from authentication.models import User

from django.core.exceptions import ObjectDoesNotExist

import utils
import logging

logger = logging.getLogger('social')


class UnfollowApiView(views.APIView):

    def post(self, request):

        ip = utils.get_client_ip(request)
        username = request.data.get('username')

        utils.start_method_log('UnfollowApiView: post',
                               authorized_user=request.user.username,
                               request_user=username)

        if username is None:
            logger.info('UnfollowApiView: post '
                        '(Username is required) username:{}, ip: {}'.format(
                            request.user.username, ip))
            return Response(
                data={"detail": "Username is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        source_user = request.User
        try:
            target_user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            logger.info('UnfollowApiView: post '
                        '(User not found) username:{}, ip: {}'.format(
                            request.user.username, ip))
            return Response(
                data={"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            followers_query_set = Followers.objects.get(
                user=source_user,
                following=target_user
            )
        except ObjectDoesNotExist:
            logger.info('UnfollowApiView: post '
                        '(You are not follow this user) username:{}, ip: {}'.format(
                            request.user.username, ip))
            return Response(
                data={"detail": "You are not follow this user"},
                status=status.HTTP_400_BAD_REQUEST
            )
        followers_query_set.delete()
        logger.info('UnfollowApiView: post '
                    '(You are successfully unfollow this user) username:{}, ip: {}'.format(
                        request.user.username, ip))
        return Response(
            data={"detail": "You are successfully unfollow this user."},
            status=status.HTTP_200_OK
        )
