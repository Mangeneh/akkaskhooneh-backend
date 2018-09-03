from rest_framework.response import Response
from rest_framework.views import APIView

import utils
from settings.base import MEDIA_URL
from social.models import Posts
from social.serializers.feed_serializer import FeedSerializer


class FeedAPI(APIView):

    def get(self, request, format=None):
        ip = utils.get_client_ip(request)
        utils.start_method_log('FeedAPI: get',
                               username=request.user.username, ip=ip)

        user = request.user

        page = request.GET.get('page')

        url = str(request.scheme) + '://' + request.get_host() + MEDIA_URL
        posts = Posts.objects.filter(owner__user=user.id).order_by("-time")
        serializer = FeedSerializer(user, context={'page': page, 'url': url, 'posts': posts})

        return Response(serializer.data)
