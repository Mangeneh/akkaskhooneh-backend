from django.db import models
from authentication.models import User
from social.models import Posts


class Board(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    class Meta:
        unique_together = ('owner', 'name')


class BoardContains(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
