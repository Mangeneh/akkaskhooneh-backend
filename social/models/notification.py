from django.db import models
from authentication.models import User
from social.models import Posts


class NotificationLike(models.Model):
    subject_user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_post = models.ForeignKey(Posts, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subject_user', 'object_post')


class NotificationFollow(models.Model):
    subject_user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subject_user', 'object_user')


class NotificationFollowRequest(models.Model):
    subject_user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subject_user', 'object_user')
