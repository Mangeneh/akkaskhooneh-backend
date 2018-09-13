import json

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
import utils
import logging
from message_queue.utils import redis_config, NotifType
from social.models import Notification, Posts

logger = logging.getLogger('social')


class SaveNotifAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):

        ip = utils.get_client_ip(request)
        utils.start_method_log("SaveNotifAPIView: post", ip=ip)

        if ip != "127.0.0.1":
            return Response(data={'detail': 'you are not allowed to view this api.'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        subject_user = data.get('subject_user')
        target_user = data.get('target_user')
        action_type = data.get('action_type')
        action_data = data.get('action_data')
        if subject_user is None \
                or target_user is None \
                or action_type is None:
            return Response({'detail': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

        if action_type == NotifType.LIKE.value and action_data is None:
            return Response({'detail': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

        if action_type == NotifType.UNLIKE.value and action_data is None:
            return Response({'detail': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

        if action_type == NotifType.COMMENT.value and action_data is None:
            return Response({'detail': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

        if action_type == NotifType.UNLIKE.value \
                or action_type == NotifType.UNFOLLOW.value \
                or action_type == NotifType.UNREQUEST.value:

            if action_type == NotifType.UNLIKE.value:
                post_id = action_data.get('post_id')
                try:
                    post = Posts.objects.get(id=post_id)
                except:
                    return Response({'detail': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    notif = Notification.objects.get(subject_user=subject_user,
                                                     target_user=target_user,
                                                     post=post,
                                                     action_type=NotifType.LIKE.value)
                except:
                    return Response({'detail': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

                notif.delete()

            if action_type == NotifType.UNFOLLOW.value:

                try:
                    notif = Notification.objects.get(subject_user=subject_user,
                                                     target_user=target_user,
                                                     action_type=NotifType.FOLLOW.value)
                except:
                    return Response({'detail': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

                notif.delete()

            if action_type == NotifType.UNREQUEST.value:
                
                try:
                    notif = Notification.objects.get(subject_user=subject_user,
                                                     target_user=target_user,
                                                     action_type=NotifType.FOLLOW_REQUEST.value)
                except:
                    return Response({'detail': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

                notif.delete()



        else:

            notif = Notification.objects.create(subject_user_id=subject_user,
                                                target_user_id=target_user,
                                                action_type=action_type)
            if action_type == NotifType.LIKE.value:
                post_id = action_data.get('post_id')
                try:
                    post = Posts.objects.get(id=post_id)
                except:
                    notif.delete()
                    return Response({'detail': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

                notif.post = post

                notif.save()

            elif action_type == NotifType.COMMENT.value:
                post_id = action_data.get('post_id')

                try:
                    post = Posts.objects.get(id=post_id)
                except:
                    notif.delete()
                    return Response({'detail': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

                notif.post = post

                ok_data = action_data.copy()
                ok_data.pop('post_id')

                notif.action_data = json.dumps(ok_data)
                notif.save()

        return Response({}, status=status.HTTP_200_OK)
