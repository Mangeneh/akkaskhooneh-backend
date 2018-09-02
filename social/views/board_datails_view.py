from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import utils
from settings.base import MEDIA_URL
from social.models import Board, Followers, BoardContains
import logging

logger = logging.getLogger('social')


class BoardDetailsAPI(APIView):
    """
    Retrieve a profile instance.
    """

    def _can_see(self, request, board_id):
        ip = utils.get_client_ip(request)

        utils.start_method_log('BoardDetailsAPI: _can_see',
                               username=request.user.username, ip=ip)
        try:
            board = Board.objects.get(id=board_id)
        except:
            return False

        if board.owner.id == request.user.id:
            return True

        flw = Followers.objects.filter(user=request.user).filter(following=board.owner)

        if len(flw) != 0:
            return True

        if not board.owner.is_private:
            return True

        return False

    def get(self, request, board_id=None, format=None):

        ip = utils.get_client_ip(request)

        utils.start_method_log('ProfileViewSet: get',
                               username=request.user.username, ip=ip)

        if (not self._can_see(request, board_id)) or board_id is None:
            logger.info('BoardDetailsAPI: get (Permission denied!)'
                        'username: {}, ip{}'.format(request.user.username, ip))
            data = {'details': 'Permission denied!'}

            return Response(data, status.HTTP_400_BAD_REQUEST)

        posts = BoardContains.objects.filter(board=board_id).values('post_id', 'post__picture')
        utils.paginator(posts)

        page = request.GET.get('page')
        pages = utils.paginator(posts, page=page)
        results = pages.get('result')
        count = pages.get('count')
        total_page = pages.get('total_page')
        results_list = []
        for post in results:
            item = {
                "id": post.get('post_id'),
                "picture": str(request.scheme) + "://" + request.get_host() +
                           MEDIA_URL + str(post.get('post__picture'))
            }
            results_list.append(item)
        data = {
            "count": count,
            "total_page": total_page,
            "results": results_list
        }
        return Response(data=data, status=status.HTTP_200_OK)
