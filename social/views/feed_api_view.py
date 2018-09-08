from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

import utils
from settings.base import MEDIA_URL
from social.models import Posts
from social.serializers import GetPostsSerializer


class FeedAPI(APIView):

    def get(self, request, format=None):
        ip = utils.get_client_ip(request)
        utils.start_method_log('FeedAPI: get',
                               username=request.user.username, ip=ip)

        user = request.user

        page = request.GET.get('page')

        url = str(request.scheme) + '://' + request.get_host() + MEDIA_URL
        posts = Posts.objects.filter(Q(owner__following__user=user) | Q(owner=user)).order_by("-time")
        serializer = GetPostsSerializer(user, context={'page': page, 'url': url, 'posts': posts})

        return Response(serializer.data)
