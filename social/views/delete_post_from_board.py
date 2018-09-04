from django.core.exceptions import ValidationError
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

import utils
from social.models import Posts, Board, Followers, BoardContains
import logging

logger = logging.getLogger('social')


class DeletePostFromBoard(APIView):
    http_method_names = ['post']
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def _validate_data(request, data):
        ip = utils.get_client_ip(request)
        utils.start_method_log('DeletePostFromBoard: _validate_data',
                               username=request.user.username, ip=ip)

        post_id = data.get('post_id')
        board_id = data.get('board_id')

        if post_id is None:
            raise ValidationError('post_id must be set.')
        if board_id is None:
            raise ValidationError('board_id must be set.')

        try:
            board = Board.objects.get(id=board_id)
        except:
            raise ValidationError('board does not exist')

        try:
            post = Posts.objects.get(id=post_id)
        except:
            raise ValidationError('post does not exist')

        if board.owner != request.user:
            raise ValidationError("it's not your board!")

        is_existed = BoardContains.objects.filter(board=board_id, post=post_id)
        if len(is_existed) == 0:
            raise ValidationError("This board doesnt have this post")

        return True

    def post(self, request):

        ip = utils.get_client_ip(request)

        utils.start_method_log('DeletePostFromBoard: post', username=request.user.username, ip=ip)

        data = request.data
        errors = {}

        try:
            DeletePostFromBoard._validate_data(request, data)
        except ValidationError as e:
            errors['details'] = list(e.messages)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        board_id = data.get('board_id')
        post_id = data.get('post_id')
        post = Posts.objects.get(id=post_id)
        board = Board.objects.get(id=board_id)

        BoardContains.objects.filter(post=post, board=board).delete()

        logger.info('DeleteNewPostFromBoard: post!'
                    'post: {post} deleted from'
                    'board: {board},'
                    'username: {username},'
                    'ip:{ip}'.format(post=post_id,
                                     board=board_id,
                                     username=request.user.username,
                                     ip=ip))
        r_data = {'details': 'Post deleted from board'}

        return Response(r_data, status.HTTP_200_OK)
