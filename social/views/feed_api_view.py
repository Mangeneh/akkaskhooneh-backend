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

        posts_of_followers = Posts.objects.filter(owner__following__user=user)
        posts_of_user = Posts.objects.filter(owner=user)
        posts = (posts_of_followers | posts_of_user).distinct().order_by("-time")

        serializer = GetPostsSerializer(user, context={'page': page, 'url': url, 'posts': posts, 'user': user})

        return Response(serializer.data)
