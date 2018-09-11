from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
import utils
import logging


logger = logging.getLogger('social')


class SaveNotifAPIView(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):

        ip = utils.get_client_ip(request)
        utils.start_method_log("SaveNotifAPIView: post", ip=ip)

        if ip != "127.0.0.1":
            return Response(data={'detail':'you are not allowed to view this api.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.POST.copy()

        subject_user = data.get('subject_user')
        target_user = data.get('target_user')
        action_type = data.get('action_type')
        action_data = data.get('action_data')

        if subject_user is None \
                or target_user is None \
                or action_type is None:
            return Response(data={'detail':'bad request'}, status=status.HTTP_400_BAD_REQUEST)

        if action_type == NotifType.LIKE.value and action_data is None:
            return Response(data={'detail':'bad request'}, status=status.HTTP_400_BAD_REQUEST)

        if action_type == NotifType.COMMENT.value and action_data is None:
            return Response(data={'detail':'bad request'}, status=status.HTTP_400_BAD_REQUEST)

        notif = Notification.objects.create(subject_user_id=subject_user,
                                            target_user_id=target_user,
                                            action_type=action_type)
        if action_type == NotifType.LIKE.value:
            notif.action_data = json.dumps(action_data)
            notif.save()

        if action_type == NotifType.COMMENT.value:
            notif.action_data = json.dumps(action_data)
            notif.save()
