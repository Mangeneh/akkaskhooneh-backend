from rest_framework import serializers
from authentication.models import User
from social.models import Followers, Request, Tags, TagContains
from utils import paginator

class TagSearchSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    results = serializers.SerializerMethodField()
    total_pages = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('count', 'total_pages', 'results')

    def get_count(self, obj):
        count = self.context.get("data").count()
        return count

    def get_total_pages(self, obj):
        all = self.context.get("data")
        p = paginator(all)
        return p.get('total_page')

    def get_results(self, obj):

        page = self.context.get("page")
        url = self.context.get("url")
        all = self.context.get("data")
        requset_user = self.context.get('request_user')
        p = paginator(all, page=page)

        result = p.get('result')
        result_list = []

        for tag in result:

            item = {
                'id': tag.id,
                'name': tag.name,
            }
            result_list.append(item)

        return result_list



