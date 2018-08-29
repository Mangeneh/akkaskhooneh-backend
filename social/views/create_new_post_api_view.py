from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from social.models import Posts
import utils
import logging
from social.forms import CreateNewPost

logger = logging.getLogger('social')


class CreateNewPostAPIView(APIView):

    def post(self, request, format=None):

        ip = utils.get_client_ip(request)
        utils.start_method_log("CreateNewPostAPIView: post",
                               username=request.user.username, ip=ip)

        data = request.POST.copy()
        data['owner'] = request.user.id
        new_post = CreateNewPost(data, request.FILES)

        if new_post.is_valid():
            new_post.save()

            logger.info('CreateNewPostAPIView: post '
                '(created successfully) username:{}, ip: {}'.format(
                    request.user.username, ip))

            return Response(status=status.HTTP_201_CREATED)
        else:
            data_response = {}
            if new_post.errors.get('picture'):
                errors = []
                for item in new_post.errors['picture']:
                    errors.append(item)
                    logger.info('CreateNewPostAPIView: post ({item}) username:{user}, ip: {ip}'.format(
                        item=item, user=request.user.username, ip=ip))
                data_response['picture'] = errors
            
            if new_post.errors.get('caption'):
                errors = []
                for item in new_post.errors['caption']:
                    errors.append(item)
                    logger.info('CreateNewPostAPIView: post ({item}) username:{user}, ip: {ip}'.format(
                        item=item, user=request.user.username, ip=ip))
                data_response['caption'] = errors

            return Response(data_response , status=status.HTTP_400_BAD_REQUEST)
