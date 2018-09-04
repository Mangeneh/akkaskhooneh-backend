from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import utils
from authentication.models import User
from social.models import  Followers
from social.serializers.user_boards_serializer import UserBoardsSerializer
from settings.base import MEDIA_URL
from social.models import Board

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

        if user != request.user and user.is_private == True:
            Flw = Followers.objects.filter(user=request.user, following=user)
            if len(Flw) == 0:
                return Response({'details': 'you cant see him/her boards'}, status=status.HTTP_400_BAD_REQUEST)

        page = request.GET.get('page')
        if page is None:
            page = 1

        url = str(request.scheme) + '://' + request.get_host() + MEDIA_URL
        data = Board.objects.filter(owner=user).order_by('-id')
        serializer = UserBoardsSerializer(user, context={'page': page, 'url': url, 'data': data})
        return Response(serializer.data)
