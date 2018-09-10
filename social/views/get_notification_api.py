from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
import utils
from settings.base import MEDIA_URL
from social.models import Posts, Notification
from social.serializers import GetPostsSerializer
from social.serializers.get_notification_serializer import GetNotifSerializer


class GetNotificationAPI(APIView):

    def get(self, request, format=None):
        ip = utils.get_client_ip(request)
        utils.start_method_log('GetNotificationAPI: get',
                               username=request.user.username, ip=ip)

        user = request.user

        page = request.GET.get('page')

        url = str(request.scheme) + '://' + request.get_host() + MEDIA_URL

        notifs = Notification.objects.filter(target_user_id=user.id).order_by('-time')

        serializer = GetNotifSerializer(user, context={'page': page, 'url': url, 'notifs': notifs})

        return Response(serializer.data)
