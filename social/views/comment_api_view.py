from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import utils
from social.models import Posts, Comment, Followers
from message_queue.add_to_redis import comment_notification

class CommentAPIView(APIView):
    @staticmethod
    def _validate_data(request, data):
        ip = utils.get_client_ip(request)
        utils.start_method_log('CommentApiView: _validate_data',
                               username=request.user.username, ip=ip)

        post_id = data.get('post_id')
        content = data.get('content')
        user_id = request.user.id

        if post_id is None:
            raise ValidationError('post_id must be set.')

        if content is None or len(content) == 0:
            raise ValidationError('content must be set.')

        if len(content) > 1000:
            raise ValidationError('content is too big.')

        try:
            post = Posts.objects.get(id=post_id)
        except:
            raise ValidationError('post does not exists')

        if not post.owner.is_private:
            return True

        if post.owner == request.user:
            return True

        flw = Followers.objects.filter(user=user_id, following=post.owner).all()
        if len(flw) != 0:
            return True

        raise ValidationError('Permission denied')

    def post(self, request, format=None):
        ip = utils.get_client_ip(request)

        utils.start_method_log('likeAPI: get',
                               username=request.user.username, ip=ip)

        data = request.data
        errors = {}

        try:
            CommentAPIView._validate_data(request, data)
        except ValidationError as e:
            errors['details'] = list(e.messages)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        post_id = data.get('post_id')
        content = data.get('content')
        post = Posts.objects.get(id=post_id)

        try:
            comment = Comment.objects.create(user=request.user, post=post, content=content)
        except:
            return Response({"details": 'comment already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        print(comment_notification(request.user.id, post.owner.id, post.id, content))
        return Response({'details': 'created'}, status=status.HTTP_201_CREATED)
