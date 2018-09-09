from .utils import NotifType
import redis
from .utils import redis_config,
from authentication.models import User
from social.models import Posts
import json

r = redis.Redis(**redis_config)


def like_notification(subject_user, target_user, post_id):
    _subject_user = User.objects.filter(id=subject_user)
    _target_user = User.objects.filter(id=target_user)
    _post_id = Posts.objects.filter(id=post_id)

    if _subject_user is None \
            or _target_user is None \
            or _post_id is None:
        return False

    data = {
        'subject_user': subject_user,
        'target_user': target_user,
        'action_data': {
            'post_id': post_id
        },
        'action_type': NotifType.LIKE.value
    }
    json_data = json.dumps(data)
    r.rpush('notification', json_data)
    return True


def follow_notification(subject_user, target_user):
    _subject_user = User.objects.filter(id=subject_user)
    _target_user = User.objects.filter(id=target_user)

    if _subject_user is None \
            or _target_user is None:
        return False

    data = {
        'subject_user': subject_user,
        'target_user': target_user,
        'action_type': NotifType.FOLLOW.value
    }
    json_data = json.dumps(data)
    r.rpush('notification', json_data)

    return True


def follow_request_notification(subject_user, target_user):
    _subject_user = User.objects.filter(id=subject_user)
    _target_user = User.objects.filter(id=target_user)

    if _subject_user is None \
            or _target_user is None:
        return False

    data = {
        'subject_user': subject_user,
        'target_user': target_user,
        'action_type': NotifType.FOLLOW_REQUEST.value
    }
    json_data = json.dumps(data)
    r.rpush('notification', json_data)

    return True


def comment_notification(subject_user, target_user, post_id,
                         comment_content):
    _subject_user = User.objects.filter(id=subject_user)
    _target_user = User.objects.filter(id=target_user)
    _post_id = Posts.objects.filter(id=post_id)

    if _subject_user is None \
            or _target_user is None \
            or _post_id is None \
            or comment_content is None \
            or type(comment_content) != str \
            or comment_content != "":
        return False

    data = {
        'subject_user': subject_user,
        'target_user': target_user,
        'action_data': {
            'post_id': post_id,
            'comment_content': comment_content
        },
        'action_type': NotifType.LIKE.value
    }
    json_data = json.dumps(data)
    r.rpush('notification', json_data)
    return True
