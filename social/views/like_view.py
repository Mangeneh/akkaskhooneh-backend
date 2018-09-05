from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import utils
from social.models import Posts, Like, Followers


class LikeAPI(APIView):
    @staticmethod
    def _validate_data(request, data):
        ip = utils.get_client_ip(request)
        utils.start_method_log('AddNewPostToBoard: _validate_data',
                               username=request.user.username, ip=ip)

        post_id = data.get('post_id')
        user_id = request.user.id

        if post_id is None:
            raise ValidationError('post_id must be set.')

        try:
            post = Posts.objects.get(id=post_id)
        except:
            raise ValidationError('post is not exists')

        if not post.owner.is_private:
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
            LikeAPI._validate_data(request, data)
        except ValidationError as e:
            errors['details'] = list(e.messages)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        post_id = data.get('post_id')
        post = Posts.objects.get(id=post_id)

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()

        return Response({'liked': created}, status=status.HTTP_200_OK)
