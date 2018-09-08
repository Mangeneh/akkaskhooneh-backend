from functools import reduce

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from operator import and_, or_

import utils
from authentication.models import User
from social.models import Followers
from social.serializers.user_search_serializer import UserSearchSerializer
from settings.base import MEDIA_URL


class FollowerSearchApiView(APIView):

    def get(self, request, username, format=None):

        ip = utils.get_client_ip(request)

        utils.start_method_log('FollowerSearchApiView: get',
                               username=request.user.username, ip=ip)

        page = request.GET.get('page')
        search_value = request.GET.get('search')

        user = User.objects.filter(username=username).first()
        if user is None:
            response_content = {"detail": "User not found."}
            return Response(response_content, status.HTTP_400_BAD_REQUEST)

        if search_value is None:
            search_value = ''

        if user != request.user and user.is_private == True:
            if Followers.objects.filter(user=request.user, following=user).count() == 0:
                return Response({'details': 'You cannot see him/her followers.'}, status=status.HTTP_400_BAD_REQUEST)

        search_array = search_value.split(' ')
        followers_query_set = Followers.objects.filter(following=user).order_by('-id')

        followers = [' ']
        for f in followers_query_set:
            followers.append(f.user.username)

        Users = User.objects.filter(reduce(or_, [Q(username=q) for q in followers])).order_by('-id')
        data = Users.filter(Q(username__icontains=search_value) | Q(reduce(or_, [Q(fullname__icontains=q) for q in search_array]))).order_by('-id')

        url = str(request.scheme) + '://' + request.get_host() + MEDIA_URL
        serializer = UserSearchSerializer(self.request.user, context={'page': page, 'url': url, 'data': data,'request_user': self.request.user})
        return Response(serializer.data)
