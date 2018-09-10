import redis
import json
from message_queue.utils import redis_config
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
django.setup()

from social.models import Notification
from message_queue.utils import NotifType

r = redis.Redis(**redis_config)


def run():
    while True:
        json_data = r.brpop('notification')
        ok_data = json_data[1].decode('utf-8')
        data = json.loads(ok_data)

        subject_user = data.get('subject_user')
        target_user = data.get('target_user')
        action_type = data.get('action_type')
        action_data = data.get('action_data')

        if subject_user is None \
                or target_user is None \
                or action_type is None:
            continue

        if action_type == NotifType.LIKE.value and action_data is None:
            continue

        if action_type == NotifType.COMMENT.value and action_data is None:
            continue

        notif = Notification.objects.create(subject_user_id=subject_user,
                                            target_user_id=target_user,
                                            action_type=action_type)
        if action_type == NotifType.LIKE.value:
            notif.action_data = action_data
            notif.save()

        if action_type == NotifType.COMMENT.value:
            notif.action_data = action_data
            notif.save()


if __name__ == '__main__':
    run()
