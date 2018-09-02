from rest_framework import views, status
from rest_framework.response import Response
from social.models import Board
from social.forms import CreateNewBoardForm
from social.serializers.create_new_board import CreateNeqBoardSerializer
import logging
import utils


logger = logging.getLogger('social')


class CreateNewBoardApiView(views.APIView):

    def post(self, request):

        ip = utils.get_client_ip(request)
        utils.start_method_log("CreateNewBoardApiView: post",
                               username=request.user.username, ip=ip)

        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = CreateNeqBoardSerializer(data=data)

        if serializer.is_valid():
            board = Board(
                owner=request.user,
                name= serializer.data.get('name')
                )
            board.save()
            logger.info('CreateNewBoardApiView: post '
                '(created successfully) username:{}, ip: {}'.format(
                    request.user.username, ip))
            return Response(
                data={
                    "id": board.id
                },
                status=status.HTTP_201_CREATED
                )
        else:
            logger.info('CreateNewBoardApiView: post '
                '(Request is not good.) username:{}, ip: {}'.format(
                    request.user.username, ip))
            return Response(status=status.HTTP_400_BAD_REQUEST)
