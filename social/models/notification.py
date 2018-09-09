from django.db import models
from authentication.models import User
from social.models import Posts


class Notification(models.Model):
    subject_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subject_user')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target_user')
    action_type = models.IntegerField()
    action_data = models.CharField(max_length=2048)
    time = models.DateTimeField(auto_now_add=True)
