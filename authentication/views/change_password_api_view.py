from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import UserChangePasswordSerializer
import utils
import logging

logger = logging.getLogger('authentication')


class ChangePassword(APIView):
    http_method_names = ['put']
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):

        ip = utils.get_client_ip(request)

        utils.start_method_log('ChangePassword: put', username=request.user.username, ip=ip)

        object = self.get_object()
        serializer = UserChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            if not object.check_password(old_password):
                logger.info('ChangePassword: put (username: {} old password is wrong  ip: {})'.format(request.user.username, ip))

                return Response({"details": ["The old password was wrong!"]},
                                status=status.HTTP_400_BAD_REQUEST)

            object.set_password(new_password)
            object.save()

            logger.info('ChangePassword: put (username: {} password changed! ip: {})'.format(request.user.username, ip))

            res = {'details': 'The password changed.'}
            return Response(res, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
