from rest_framework import status, views
from rest_framework.response import Response

import utils
from social.models import Posts, Followers
from authentication.models import User
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
            username = request.user.username
        try:
            profile = User.objects.get(username=username)
        except ObjectDoesNotExist:
            data = {
                "error": "Username not found"
            }
            logger.info('PaginationApiView: get '
                        '(Username not found) username:{}, ip: {}'.format(
                            request.user.username, ip))
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        profile_private = profile.is_private
        target_profile = profile
        user_profile = request.user
        if target_profile != user_profile and profile_private:
            try:
                follow_status = Followers.objects.get(
                    user=user_profile,
                    following=target_profile
                )
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_403_FORBIDDEN)

        queryset = Posts.objects.filter(owner=profile).order_by('-time')

        page = request.GET.get('page')
        pages = utils.paginator(queryset, page=page)
        results = pages.get('result')
        count = pages.get('count')
        total_page = pages.get('total_page')
        results_list = []
        for post in results:
            item = {
                "id": post.id,
                "post_picture": str(request.scheme) + "://" + request.get_host() +
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
