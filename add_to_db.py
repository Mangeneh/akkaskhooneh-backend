import redis
import json
from message_queue.utils import redis_config, NotifType
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
django.setup()

from social.models import Notification, Posts

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

        if action_type == NotifType.UNLIKE.value and action_data is None:
            continue

        if action_type == NotifType.COMMENT.value and action_data is None:
            continue

        if action_type == NotifType.UNLIKE.value \
                or action_type == NotifType.UNFOLLOW.value \
                or action_type == NotifType.UNREQUEST.value:

            if action_type == NotifType.UNLIKE.value:
                post_id = action_data.get('post_id')
                try:
                    post = Posts.objects.get(id=post_id)
                except:
                    continue
                try:
                    notif = Notification.objects.get(subject_user=subject_user,
                                                     target_user=target_user,
                                                     post=post,
                                                     action_type=NotifType.LIKE.value)
                except:
                    continue

                notif.delete()

            if action_type == NotifType.UNFOLLOW.value:

                try:
                    notif = Notification.objects.get(subject_user=subject_user,
                                                     target_user=target_user,
                                                     action_type=NotifType.FOLLOW.value)
                except:
                    continue

                notif.delete()

            if action_type == NotifType.UNREQUEST.value:

                try:
                    notif = Notification.objects.get(subject_user=subject_user,
                                                     target_user=target_user,
                                                     action_type=NotifType.FOLLOW_REQUEST)
                except:
                    continue

                notif.delete()



        else:

            notif = Notification.objects.create(subject_user_id=subject_user,
                                                target_user_id=target_user,
                                                action_type=action_type)
            if action_type == NotifType.LIKE.value:
                post_id = action_data.get('post_id')
                try:
                    post = Posts.objects.get(id=post_id)
                except:
                    notif.delete()
                    continue

                notif.post = post

                notif.save()

            elif action_type == NotifType.COMMENT.value:
                post_id = action_data.get('post_id')

                try:
                    post = Posts.objects.get(id=post_id)
                except:
                    notif.delete()
                    continue

                notif.post = post

                ok_data = action_data.copy()
                ok_data.pop('post_id')

                notif.action_data = json.dumps(ok_data)
                notif.save()


if __name__ == '__main__':
    run()
