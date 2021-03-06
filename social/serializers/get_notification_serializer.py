from rest_framework import serializers

from authentication.models import User
from social.models import Like, Comment, Posts
from message_queue.utils import NotifType
from utils import paginator
import json


class GetNotifSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    results = serializers.SerializerMethodField()
    total_pages = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('count', 'results', 'total_pages')

    def get_count(self, obj):
        count = self.context.get('notifs').count()
        return count

    def get_total_pages(self, obj):
        all = self.context.get('notifs')
        p = paginator(all, limit=15)

        return p.get('total_page')

    def get_results(self, obj):
        page = self.context.get("page")
        url = self.context.get("url")
        all = self.context.get("notifs")
        user = self.context.get('user')
        p = paginator(all, page=page, limit=15)

        result = p.get('result')
        result_list = []
        for notif in result:
            data = {}

            if notif.action_type == NotifType.LIKE.value or \
                    notif.action_type == NotifType.COMMENT.value:
                data['post_picture'] = url + str(notif.post.picture)
                data['post_id'] = notif.post.id

            if notif.action_type == NotifType.OTHER_FOLLOW.value:
                action_data = json.loads(notif.action_data)
                id = action_data['other_user']
                username = User.objects.get(id=id).username
                data['username'] = username

            item = {
                'subject_user': notif.subject_user.username,
                'notif_type': notif.action_type,
                'profile_picture': url + str(notif.subject_user.profile_picture),
                'time': notif.time,
                'data': data
            }
            result_list.append(item)
        return result_list
