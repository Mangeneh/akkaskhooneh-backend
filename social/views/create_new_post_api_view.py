from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from social.models import Posts
import utils
import logging

logger = logging.getLogger('social')


class CreateNewPostAPIView(APIView):

    def post(self, request, format=None):

        ip = utils.get_client_ip(request)

        utils.start_method_log('CreateNewPostAPIView: post', username=request.user.username, ip=ip)

        user = request.user
        picture = request.FILES.get('picture')
        caption = request.POST.copy().get('caption')

        if user is None:
            logger.info('CreateNewPostAPIView: post (user is not authorized) ip: {}'.format(ip))

            res = {'details': 'user is not authorized'}
            return Response(res, status.HTTP_400_BAD_REQUEST)
        if picture is None:
            logger.info('CreateNewPostAPIView: post'
                        ' (picture not found) username:{}, ip: {}'.format(user.username, ip))

            res = {'details': 'picture not found'}
            return Response(res, status.HTTP_400_BAD_REQUEST)

        post = Posts.objects.create(owner=user, picture=picture, caption=caption)
        post.save()

        logger.info('CreateNewPostAPIView: post'
                    ' (created successfully) username:{}, ip: {}'.format(user.username, ip))

        res = {'details': 'created successfully'}
        return Response(res, status.HTTP_201_CREATED)
