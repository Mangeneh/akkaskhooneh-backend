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
        p = paginator(all, page=page)

        result = p.get('result')
        result_list = []
        for post in result:
            item = {
                'id': post.id,
                'owner_username': post.owner.username,
                'profile_picture': url + str(post.owner.profile_picture),
                'post_picture': url + str(post.picture),
                'caption': post.caption if post.caption is not None else "",
                'likes': Like.objects.filter(post=post).count(),
                'comments': Comment.objects.filter(post=post).count(),
                'time': post.time,
            }
            result_list.append(item)

        return result_list
