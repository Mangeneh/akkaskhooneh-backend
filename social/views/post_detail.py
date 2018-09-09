from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from social.models import Posts, Followers, Like, Comment, TagContains
from django.core.exceptions import ObjectDoesNotExist
from settings.base import MEDIA_URL


class PostDetailApiView(APIView):

    def get(self, request, id, format=None):

        try:
            post = Posts.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        profile_private = post.owner.is_private
        if profile_private:
            post_owner = post.owner
            user_profile = request.user
            try:
                follow_status = Followers.objects.get(
                    user=user_profile,
                    following=post_owner
                )
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_403_FORBIDDEN)
        likes_count = Like.objects.filter(post=post).count()
        comments_count = Comment.objects.filter(post=post).count()
        tags_query_set = TagContains.objects.filter(post=post)
        tags_list = []
        for tag in tags_query_set:
            tags_list.append(tag.tag.name)
        url = str(request.scheme) + '://' + request.get_host() + MEDIA_URL
        try:
            is_liked_query_set = Like.objects.get(user=request.user, post=post)
            is_liked = True
        except ObjectDoesNotExist:
            is_liked = False

        data = {
            "picture": url + str(post.picture),
            "caption": post.caption,
            "is_liked": is_liked,
            "likes_count": likes_count,
            "comments_count": comments_count,
            "tags_list": tags_list,
            "profile_picture": url + str(post.owner.profile_picture),
            "username": post.owner.username,
            "time": post.time
        }

        return Response(data=data, status=status.HTTP_200_OK)
