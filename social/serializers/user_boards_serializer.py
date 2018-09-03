from rest_framework import serializers
from authentication.models import User
from social.models import Board, BoardContains
from utils import paginator

class UserBoardsSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    paginator = serializers.SerializerMethodField()
    total_pages = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('count', 'paginator', 'total_pages')

    def get_count(self, obj):
        count = self.context.get("data").count()
        return count

    def get_total_pages(self, obj):
        all = self.context.get("data")
        p = paginator(all)
        return p.get('total_page')

    def get_paginator(self, obj):

        page = self.context.get("page")
        url = self.context.get("url")
        all = self.context.get("data")
        p = paginator(all, page=page)

        result = p.get('result')
        result_list = []

        for board in result:
            last_posts = BoardContains.objects.filter(board=board).order_by('-id')[:5]
            last_pics = []

            for postcontains in last_posts:
                post = postcontains.post
                last_pics.append(url + str(post.picture))

            item = {
                'id': board.id,
                'name': board.name,
                'count': BoardContains.objects.filter(board=board).count(),
                'last_pics': last_pics
            }
            result_list.append(item)

        return result_list



