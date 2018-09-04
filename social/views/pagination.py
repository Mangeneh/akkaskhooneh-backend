from rest_framework import status, views
from rest_framework.response import Response

import utils
from social.models.posts import Posts
from authentication.models.user import User
from django.core.exceptions import ObjectDoesNotExist
from settings.base import MEDIA_URL
import logging

logger = logging.getLogger('social')

class PaginationApiView(views.APIView):

    def get(self, request, username=None, *args, **kwargs):

        ip = utils.get_client_ip(request)

        utils.start_method_log('PaginationApiView: get',
                               authorized_user=request.user.username,
                               request_user=username)


        if username is None:
            username = request.user.id
        else:
            try:
                username = User.objects.get(username=username)
            except ObjectDoesNotExist:
                data = {
                    "error": "Username not found"
                }
                logger.info('PaginationApiView: get '
                    '(Username not found) username:{}, ip: {}'.format(
                        request.user.username, ip))
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        queryset = Posts.objects.filter(owner=username).order_by('-time')

        page = request.GET.get('page')
        pages = utils.paginator(queryset, page=page)
        results = pages.get('result')
        count = pages.get('count')
        total_page = pages.get('total_page')
        results_list = []
        for post in results:
            item = {
                "id": post.id,
                "picture": str(request.scheme) + "://" + request.get_host() +
                MEDIA_URL + str(post.picture)
            }
            results_list.append(item)
        data = {
            "count": count,
            "total_pages": total_page,
            "results": results_list
        }
        logger.info('PaginationApiView: get '
                    '(get posts of {}) username:{}, ip: {}'.format(
                        username, request.user.username, ip))
        return Response(data=data, status=status.HTTP_200_OK)
