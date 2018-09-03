from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import utils
from authentication.models import User
from social.serializers.user_boards_serializer import UserBoardsSerializer
from settings.base import MEDIA_URL


class UserBoardsApiView(APIView):

    def get(self, request, username=None, format=None):

        ip = utils.get_client_ip(request)

        utils.start_method_log('BoardApiView: get',
                               username=request.user.username, ip=ip)

        user = request.user
        if username is not None:
            user = User.objects.filter(username=username).first()
            if user is None:
                response_content = {"detail": "User not found."}
                return Response(response_content, status.HTTP_400_BAD_REQUEST)

        page = request.GET.get('page')
        if page is None:
            page = 1

        url = str(request.scheme) + '://' + request.get_host() + MEDIA_URL
        serializer = UserBoardsSerializer(user, context={'page': page, 'url': url})
        return Response(serializer.data)
