from rest_framework import views, status
from rest_framework.response import Response
from social.models import Board
from social.forms import CreateNewBoardForm
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
        board = CreateNewBoardForm(data)
        if board.is_valid():
            board.save()
            logger.info('CreateNewBoardApiView: post '
                '(created successfully) username:{}, ip: {}'.format(
                    request.user.username, ip))
            return Response(status=status.HTTP_201_CREATED)
        else:
            logger.info('CreateNewBoardApiView: post '
                '(Request is not good.) username:{}, ip: {}'.format(
                    request.user.username, ip))
            return Response(status=status.HTTP_400_BAD_REQUEST)
