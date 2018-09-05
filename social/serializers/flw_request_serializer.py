from rest_framework import serializers
from social.models import  Request
from utils import paginator


class FolloweReqSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    results = serializers.SerializerMethodField()
    total_pages = serializers.SerializerMethodField()

    class Meta:
        model = Request
        fields = ('count', 'results', 'total_pages')

    def get_count(self, obj):
        count = self.context.get('requests').count()
        return count

    def get_total_pages(self, obj):
        all = self.context.get('requests')
        p = paginator(all)

        return p.get('total_page')

    def get_results(self, obj):
        page = self.context.get("page")
        url = self.context.get("url")
        all = self.context.get("requests")
        p = paginator(all, page=page)

        result = p.get('result')
        result_list = []
        for req in result:
            item = {
                'id': req.id,
                'requester_username': req.requester.username,
                'requester_username_picture': url + str(req.requester.profile_picture),
                'request_time': req.request_time,
            }
            result_list.append(item)

        return result_list
