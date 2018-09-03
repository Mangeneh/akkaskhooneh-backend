from django.core.exceptions import ValidationError
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

import utils
from social.models import Board
import logging

logger = logging.getLogger('social')


class DeleteBoard(APIView):
    http_method_names = ['delete']
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def _validate_data(request, data):
        ip = utils.get_client_ip(request)
        utils.start_method_log('DeleteBoard: _validate_data',
                               username=request.user.username, ip=ip)
        board_id = data.get('board_id')

        if board_id is None:
            raise ValidationError('board_id must be set.')
        try:
            board = Board.objects.get(id=board_id)
        except:
            raise ValidationError('board is not exists')

        if board.owner != request.user:
            raise ValidationError("it's not your board!")

    def delete(self, request):
        ip = utils.get_client_ip(request)

        utils.start_method_log('DeleteBoard: post', username=request.user.username, ip=ip)

        data = request.data
        errors = {}

        try:
            DeleteBoard._validate_data(request, data)
        except ValidationError as e:
            errors['details'] = list(e.messages)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        board_id = request.data.get('board_id')
        Board.objects.filter(id=board_id).delete()

        logger.info('DeleteBoard: delete!'
                    'board: {board},'
                    'username: {username},'
                    'ip:{ip}'.format(board=board_id,
                                     username=request.user.username,
                                     ip=ip))

        r_data = {'details': 'Board deleted'}
        return Response(r_data, status.HTTP_200_OK)
