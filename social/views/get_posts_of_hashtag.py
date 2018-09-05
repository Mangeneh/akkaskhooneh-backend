from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
import utils
from settings.base import MEDIA_URL
from social.models import Posts
from social.serializers import GetPostsSerializer


class GetPostOfTagAPI(APIView):

    def get(self, request, tag_id, format=None):
        ip = utils.get_client_ip(request)
        utils.start_method_log('GetPostOfTagAPI: get',
                               username=request.user.username, ip=ip)

        user = request.user

        page = request.GET.get('page')

        url = str(request.scheme) + '://' + request.get_host() + MEDIA_URL
        posts = Posts.objects.filter(tagcontains__tag_id=tag_id).filter(
            Q(owner__following__user=user) | Q(owner__is_private=False)).order_by("-time")
        serializer = GetPostsSerializer(user, context={'page': page, 'url': url, 'posts': posts})

        return Response(serializer.data)
