from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from social.models import Posts, Tags, TagContains
import utils
import validators
import logging
from social.forms import CreateNewPost
from django.core.exceptions import ValidationError


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
            post = Posts(
                owner = new_post.cleaned_data.get('owner'),
                picture = new_post.cleaned_data.get('picture'),
                caption = new_post.cleaned_data.get('caption')
                )
            
            tags_list = data.get('tags')
            if tags_list is not None:
                tags_list = tags_list.split(',')
                for tag_item in tags_list:
                    try:
                        validators.validate_tag(tag_item)
                    except ValidationError:
                        return Response(
                            data={"tags": "Invalid"},
                            status=status.HTTP_400_BAD_REQUEST)
                    tag,_ = Tags.objects.get_or_create(name=tag_item)
                    
                post.save()

                for tag_item in tags_list:
                    tag = Tags.objects.get(name=tag_item)
                    TagContains.objects.create(tag=tag, post=post)
            else:
                post.save()

            logger.info('CreateNewPostAPIView: post '
                    '(created successfully) username:{}, ip: {}'.format(
                        request.user.username, ip))

            return Response(
                data={"Result": "OK"},
                status=status.HTTP_201_CREATED)
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
