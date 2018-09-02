from django.db import models
from authentication.models import User
from validators import validate_image


class Posts(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner")
    picture = models.ImageField(
        upload_to="post_pictures/", validators=[validate_image])
    caption = models.CharField(max_length=1000, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
