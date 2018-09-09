from rest_framework import views, status
from rest_framework.response import Response
from social.models import Posts, Comment, Followers
from django.core.exceptions import ObjectDoesNotExist
from settings.base import MEDIA_URL
import utils
import logging

logger = logging.getLogger('social')


class GetCommentsApiView(views.APIView):
    """
    This api view return comment list of post
    """

    def get(self, request, post_id):

        ip = utils.get_client_ip(request)

        utils.start_method_log('GetCommentsApiView: get',
                               authorized_user=request.user.username,
                               request_post_id=post_id)

        if post_id is None:
            logger.info('PaginationApiView: get '
                        '(Post_id is required) username:{}, ip: {}'.format(
                            request.user.username, ip))
            return Response(
                data={"detail": "Post_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            post_query_set = Posts.objects.get(id=post_id)
        except ObjectDoesNotExist:
            logger.info('PaginationApiView: get '
                        '(Post not found) username:{}, ip: {}'.format(
                            request.user.username, ip))
            return Response(
                data={"details": "Post not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        profile_private = post.owner.is_private
        post_owner = post.owner
        user_profile = request.user
        if post_owner != user_profile and profile_private:
            try:
                follow_status = Followers.objects.get(
                    user=user_profile,
                    following=post_owner
                )
            except ObjectDoesNotExist:
                logger.info('PaginationApiView: get '
                            '(User not follow this post owner) username:{}, ip: {}'.format(
                                request.user.username, ip))
                return Response(status=status.HTTP_403_FORBIDDEN)

        comment_query_set = Comment.objects.filter(
            post=post_query_set).order_by('-time')
        page = request.data.get('page')
        pages = utils.paginator(comment_query_set, page=page)
        results = pages.get('result')
        count = pages.get('count')
        total_page = pages.get('total_page')
        results_list = []
        url = str(request.scheme) + '://' + request.get_host() + MEDIA_URL
        for cm in results:
            item = {
                "username": cm.user.username,
                "profile_picture": url + str(cm.user.profile_picture),
                "comment": cm.content,
                "time": cm.time
            }
            results_list.append(item)
        data = {
            "count": count,
            "total_pages": total_page,
            "results": results_list
        }
        logger.info('PaginationApiView: get '
                    '(Successfully return comment list) username:{}, ip: {}'.format(
                        request.user.username, ip))
        return Response(data=data, status=status.HTTP_200_OK)
