from rest_framework.response import Response
from rest_framework.views import APIView

import utils
from authentication.models import User
from social.serializers.user_search_serializer import UserSearchSerializer
from settings.base import MEDIA_URL

class UserSearchApiView(APIView):

    def get(self, request, format=None):

        ip = utils.get_client_ip(request)

        utils.start_method_log('UserSearchApiView: get',
                               username=request.user.username, ip=ip)

        page = request.GET.get('page')
        search_value = request.GET.get('search')

        if page is None:
            page = 1

        data = User.objects.filter(username__icontains=search_value).order_by('-id')
        url = str(request.scheme) + '://' + request.get_host() + MEDIA_URL
        serializer = UserSearchSerializer(self.request.user, context={'page': page, 'url': url, 'data': data,'request_user': self.request.user})
        return Response(serializer.data)
