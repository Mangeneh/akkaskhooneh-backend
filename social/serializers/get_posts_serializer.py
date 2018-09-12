from rest_framework import serializers

from authentication.models import User
from social.models import Like, Comment
from utils import paginator


class GetPostsSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    results = serializers.SerializerMethodField()
    total_pages = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('count', 'results', 'total_pages')

    def get_count(self, obj):
        count = self.context.get('posts').count()
        return count

    def get_total_pages(self, obj):
        all = self.context.get('posts')
        p = paginator(all)

        return p.get('total_page')

    def get_results(self, obj):
        page = self.context.get("page")
        url = self.context.get("url")
        all = self.context.get("posts")
        user = self.context.get('user')
        tag_search = self.context.get('tag_search')

        p = paginator(all, page=page)


        result = p.get('result')
        result_list = []
        for post in result:
            like_query = Like.objects.filter(post=post, user=user)
            is_liked = True if len(like_query) > 0 else False
            item = {}
            if tag_search == None:
                item = {
                    'id': post.id,
                    'owner_username': post.owner.username,
                    'profile_picture': url + str(post.owner.profile_picture),
                    'post_picture': url + str(post.picture),
                    'caption': post.caption if post.caption is not None else "",
                    'likes_count': Like.objects.filter(post=post).count(),
                    'comments_count': Comment.objects.filter(post=post).count(),
                    'time': post.time,
                    'is_liked': is_liked
                }
            else:
                item = {
                    'id': post.id,
                    'post_picture': url + str(post.picture)
                }
            result_list.append(item)

        return result_list
