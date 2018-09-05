from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from social.models import Posts, Tags, TagContains, Request, Followers
import utils
import logging

logger = logging.getLogger('social')


class AcceptFollowRequestAPIView(APIView):

    def post(self, request, format=None):

        ip = utils.get_client_ip(request)
        utils.start_method_log("AcceptFollowPostAPIView: post",
                               username=request.user.username, ip=ip)

        data = request.data.copy()

        if data.get('request_id') == None or data.get('accept') == None:
            return Response({'details': 'bad request!'}, status=status.HTTP_400_BAD_REQUEST)

        request_data = Request.objects.filter(id=data['request_id'])

        if len(request_data) == 0:
            return Response({'details': 'cant find this request'}, status=status.HTTP_400_BAD_REQUEST)

        requester = request_data[0].requester

        if request_data[0].requestee != request.user:
            return Response({'details': 'this is not your request'}, status=status.HTTP_400_BAD_REQUEST)

        if data['accept'] == True:
            Followers.objects.create(user=requester, following=request.user)

        request_data[0].delete()

        return Response({'succes': 'True'}, status=status.HTTP_201_CREATED)