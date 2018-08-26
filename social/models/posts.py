from django.db import models
from authentication.models import User


class Posts(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="owner"
    )
    picture = models.ImageField(upload_to="post_pictures/")
    caption = models.TextField(max_length=1023, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
