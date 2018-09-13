from rest_framework import views, status
from rest_framework.response import Response
from authentication.models import User
from social.models import Request, Followers
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from message_queue.add_to_redis import follow_notification, follow_request_notification
import logging
import utils

logger = logging.getLogger('social')


class FollowRequest(views.APIView):

    def post(self, request):

        ip = utils.get_client_ip(request)

        utils.start_method_log(
            'FollowRequest: post', ip=ip)

        target_user_name = request.data.get('username')
        if target_user_name == request.user.username:
            logger.info(
                'FollowRequest: post'
                '(You can not follow your self. '
                'username: {username}, ip: {ip})'.format(
                    ip=ip, username=request.user.username))
            return Response(
                data={"error": "you connot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if target_user_name is None:
            logger.info(
                'FollowRequest: post'
                '(Username is required.. '
                'username: {username}, ip: {ip})'.format(
                    ip=ip, username=request.user.username))
            return Response(
                data={"error": "Username is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            target_user_query_set = User.objects.get(username=target_user_name)
        except ObjectDoesNotExist:
            logger.info(
                'FollowRequest: post'
                '(User not found '
                'username: {username}, ip: {ip})'.format(
                    ip=ip, username=request.user.username))
            return Response(
                data={"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        if target_user_query_set.is_private:
            try:
                follow_status = Followers.objects.get(
                    user=request.user,
                    following=target_user_query_set
                )
                logger.info(
                    'FollowRequest: post'
                    '(You are already followed this user. '
                    'username: {username}, ip: {ip})'.format(
                        ip=ip, username=request.user.username))
                return Response(
                    data={"error": "You are already followed this user"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ObjectDoesNotExist:
                request_object, create = Request.objects.get_or_create(
                    requester=request.user,
                    requestee=target_user_query_set
                )
                if create:
                    follow_request_notification(
                        request.user.id, target_user_query_set.id)
                    logger.info(
                        'FollowRequest: post'
                        '(Follow request created. '
                        'username: {username}, ip: {ip})'.format(
                            ip=ip, username=request.user.username))
                    return Response(
                        data={"detail": "Follow request created."},
                        status=status.HTTP_201_CREATED
                    )
                else:
                    logger.info(
                        'FollowRequest: post'
                        '(You are already requested for follow this user. '
                        'username: {username}, ip: {ip})'.format(
                            ip=ip, username=request.user.username))
                    return Response(
                        data={
                            "details": "You are already requested for follow this user."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            try:
                follow_status = Followers.objects.get(
                    user=request.user,
                    following=target_user_query_set
                )
                logger.info(
                    'FollowRequest: post'
                    '(You are already follow this user. '
                    'username: {username}, ip: {ip})'.format(
                        ip=ip, username=request.user.username))
                return Response(
                    data={"error": "You are already followed this user"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ObjectDoesNotExist:
                try:
                    Followers.objects.create(
                        user=request.user,
                        following=target_user_query_set
                    )
                except IntegrityError:
                    logger.info(
                        'FollowRequest: post'
                        '(This object already exist. '
                        'username: {username}, ip: {ip})'.format(
                            ip=ip, username=request.user.username))
                    return Response(
                        data={"details": "This object already exist."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                follow_notification(request.user.id, target_user_query_set.id)
                logger.info(
                    'FollowRequest: post'
                    '(You are successfully follow this user. '
                    'username: {username}, ip: {ip})'.format(
                        ip=ip, username=request.user.username))
                return Response(
                    data={"details": "You are successfully follow this user."},
                    status=status.HTTP_201_CREATED
                )
