from django.db import models

from social.models import Posts
from validators import validate_tag


class Tags(models.Model):
    name = models.CharField(max_length=40, validators=[validate_tag])


class TagContains(models.Model):
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tag', 'post')
