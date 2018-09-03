from django.db import models
from authentication.models import User
from social.models import Posts


class Like(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='post_like')