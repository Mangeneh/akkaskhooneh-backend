import redis
from .utils import redis_config, NotifType
from authentication.models import User
from social.models import Posts, Followers
import json

r = redis.Redis(**redis_config)


def like_notification(subject_user, target_user, post_id):
    _subject_user = User.objects.filter(id=subject_user)
    _target_user = User.objects.filter(id=target_user)
    _post_id = Posts.objects.filter(id=post_id)

    if len(_subject_user) == 0 \
            or len(_target_user) == 0 \
            or len(_post_id) == 0:
        return False

    data = {
        "subject_user": subject_user,
        "target_user": target_user,
        "action_data": {
            "post_id": post_id
        },
        "action_type": NotifType.LIKE.value
    }
    json_data = json.dumps(data)
    r.rpush('notification', json_data)
    return True


def follow_notification(subject_user, target_user):
    _subject_user = User.objects.filter(id=subject_user)
    _target_user = User.objects.filter(id=target_user)

    if len(_subject_user) == 0 \
            or len(_target_user) == 0:
        return False

    followers = Followers.objects.filter(following=subject_user)
    for follower in followers:
        other_follow_notification(subject_user, follower.user.id, target_user)

    data = {
        "subject_user": subject_user,
        "target_user": target_user,
        "action_type": NotifType.FOLLOW.value
    }
    json_data = json.dumps(data)
    r.rpush('notification', json_data)

    return True


def follow_request_notification(subject_user, target_user):
    _subject_user = User.objects.filter(id=subject_user)
    _target_user = User.objects.filter(id=target_user)

    if len(_subject_user) == 0 \
            or len(_target_user) == 0:
        return False

    data = {
        "subject_user": subject_user,
        "target_user": target_user,
        "action_type": NotifType.FOLLOW_REQUEST.value
    }
    json_data = json.dumps(data)
    r.rpush('notification', json_data)

    return True


def comment_notification(subject_user, target_user, post_id,
                         comment_content):
    _subject_user = User.objects.filter(id=subject_user)
    _target_user = User.objects.filter(id=target_user)
    _post_id = Posts.objects.filter(id=post_id)

    if len(_subject_user) == 0 \
            or len(_target_user) == 0 \
            or len(_post_id) == 0 \
            or comment_content is None \
            or type(comment_content) != str \
            or comment_content == "":
        return False

    data = {
        "subject_user": subject_user,
        "target_user": target_user,
        "action_data": {
            "post_id": post_id,
            "comment_content": comment_content
        },
        "action_type": NotifType.COMMENT.value
    }
    json_data = json.dumps(data)
    r.rpush('notification', json_data)
    return True


def unlike_notification(subject_user, target_user, post_id):
    _subject_user = User.objects.filter(id=subject_user)
    _target_user = User.objects.filter(id=target_user)
    _post_id = Posts.objects.filter(id=post_id)

    if len(_subject_user) == 0 \
            or len(_target_user) == 0 \
            or len(_post_id) == 0:
        return False

    data = {
        "subject_user": subject_user,
        "target_user": target_user,
        "action_data": {
            "post_id": post_id
        },
        "action_type": NotifType.UNLIKE.value
    }
    json_data = json.dumps(data)
    r.rpush('notification', json_data)
    return True


def unfollow_notification(subject_user, target_user):
    _subject_user = User.objects.filter(id=subject_user)
    _target_user = User.objects.filter(id=target_user)

    if len(_subject_user) == 0 \
            or len(_target_user) == 0:
        return False

    followers = Followers.objects.filter(following=subject_user)
    for follower in followers:
        unother_follow_notification(subject_user, follower.user.id, target_user)

    data = {
        "subject_user": subject_user,
        "target_user": target_user,
        "action_type": NotifType.UNFOLLOW.value
    }
    json_data = json.dumps(data)
    r.rpush('notification', json_data)

    return True


def unfollow_request_notification(subject_user, target_user):
    _subject_user = User.objects.filter(id=subject_user)
    _target_user = User.objects.filter(id=target_user)

    if len(_subject_user) == 0 \
            or len(_target_user) == 0:
        return False

    data = {
        "subject_user": subject_user,
        "target_user": target_user,
        "action_type": NotifType.UNREQUEST.value
    }
    json_data = json.dumps(data)
    r.rpush('notification', json_data)

    return True


def other_follow_notification(subject_user, target_user, other_user):
    _subject_user = User.objects.filter(id=subject_user)
    _target_user = User.objects.filter(id=target_user)
    _other_user = User.objects.filter(id=other_user)
    if len(_subject_user) == 0 \
            or len(_target_user) == 0 \
            or len(_other_user) == 0:
        return False

    data = {
        "subject_user": subject_user,
        "target_user": target_user,
        "action_type": NotifType.OTHER_FOLLOW.value,
        "action_data": {
            "other_user": other_user
        },
    }
    json_data = json.dumps(data)
    r.rpush('notification', json_data)

    return True

def unother_follow_notification(subject_user, target_user, other_user):
    _subject_user = User.objects.filter(id=subject_user)
    _target_user = User.objects.filter(id=target_user)
    _other_user = User.objects.filter(id=other_user)
    if len(_subject_user) == 0 \
            or len(_target_user) == 0 \
            or len(_other_user) == 0:
        return False

    data = {
        "subject_user": subject_user,
        "target_user": target_user,
        "action_type": NotifType.UNOTHER_FOLLOW.value,
        "action_data": {
            "other_user": other_user
        },
    }
    json_data = json.dumps(data)
    r.rpush('notification', json_data)

    return True
