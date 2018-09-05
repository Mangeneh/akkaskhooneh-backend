from rest_framework.response import Response
from rest_framework.views import APIView

import utils
from settings.base import MEDIA_URL
from social.models import Posts
from social.serializers import GetPostsSerializer, FolloweReqSerializer
from social.models import Request


class GetFollowReqAPI(APIView):

    def get(self, request, format=None):
        ip = utils.get_client_ip(request)
        utils.start_method_log('GetFollowReqAPI: get',
                               username=request.user.username, ip=ip)

        user = request.user

        page = request.GET.get('page')

        url = str(request.scheme) + '://' + request.get_host() + MEDIA_URL
        requests = Request.objects.filter(requestee=request.user).order_by("-request_time")
        serializer = FolloweReqSerializer(user, context={'page': page, 'url': url, 'requests': requests})

        return Response(serializer.data)
