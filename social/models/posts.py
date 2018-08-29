from django.db import models
from authentication.models import User
from django.core.exceptions import ValidationError


class Posts(models.Model):

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" %
                                  str(megabyte_limit))

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner")
    picture = models.ImageField(
        upload_to="post_pictures/", validators=[validate_image])
    caption = models.TextField(max_length=1023, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
