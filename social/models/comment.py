from django.db import models
from authentication.models import User
from social.models import Posts


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_comment')
    post = models.ForeignKey(
        Posts, on_delete=models.CASCADE, related_name='post_comment')
    content = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post', 'content')
