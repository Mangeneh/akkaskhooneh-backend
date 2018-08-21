from django.db import models
from authentication.models import User


class Followers(models.Model):
    """
    This model use for followers and following for users.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
