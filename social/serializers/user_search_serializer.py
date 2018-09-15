from rest_framework import serializers
from authentication.models import User
from social.models import Followers, Request
from utils import paginator


class UserSearchSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    results = serializers.SerializerMethodField()
    total_pages = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('count', 'total_pages', 'results')

    def get_count(self, obj):
        count = len(self.context.get("data"))
        return count

    def get_total_pages(self, obj):
        all = self.context.get("data")
        p = paginator(all, limit=15)
        return p.get('total_page')

    def get_results(self, obj):

        page = self.context.get("page")
        url = self.context.get("url")
        all = self.context.get("data")
        requset_user = self.context.get('request_user')
        p = paginator(all, page=page, limit=15)

        result = p.get('result')
        result_list = []

        for user in result:

            follow_state = 3
            is_followed = Followers.objects.filter(
                user=requset_user, following=user)

            if len(is_followed):
                follow_state = 1

            is_requested = Request.objects.filter(
                requester=requset_user, requestee=user)
            if len(is_requested):
                follow_state = 2

            item = {
                'username': user.username,
                'is_private': user.is_private,
                'profile_picture': url + str(user.profile_picture),
                'fullname': user.fullname if user.fullname is not None else "",
                'following_status': follow_state
            }
            result_list.append(item)

        return result_list
