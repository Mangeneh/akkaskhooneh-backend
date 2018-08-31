from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from authentication.managers import UserManager
from django.core.exceptions import ValidationError
from PIL import Image


class User(AbstractBaseUser, PermissionsMixin):

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 3.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" %
                                  str(megabyte_limit))

        im = Image.open(fieldfile_obj.file)
        width, height = im.size
        if width > 1080 or height > 1080:
            raise ValidationError("Maximum file resolution is 1080.")

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    fullname = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profiles/", default='user.png', validators=[validate_image])
    bio = models.CharField(max_length=300, blank=True, null=True)
    phone_number = models.CharField(
        max_length=30, unique=True, blank=True, null=True)
    register_date = models.DateField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return "Username: {}, Email: {}".format(self.username, self.email)

    def get_full_name(self):
        return self.fullname

    def get_bio(self):
        return self.bio
