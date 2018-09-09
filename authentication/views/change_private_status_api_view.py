from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from social.models import Request, Followers
import utils
import logging

logger = logging.getLogger('authentication')


class ChangePrivateStatus(APIView):
    http_method_names = ['post']
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        ip = utils.get_client_ip(request)

        utils.start_method_log('ChangePrivateStatus: post', username=request.user.username, ip=ip)

        user = self.request.user

        if user.is_private:
            requests = Request.objects.filter(requestee=user)
            for req in requests:
                try:
                    Followers.objects.create(user=req.requester, following=req.requestee)
                except:
                    pass
                req.delete()
            user.is_private = False
            user.save()
            return Response(data={'detail':'user is public now'}, status=status.HTTP_200_OK)
        else:
            user.is_private = True
            user.save()
            return Response(data={'detail':'user is private now'}, status=status.HTTP_200_OK)

