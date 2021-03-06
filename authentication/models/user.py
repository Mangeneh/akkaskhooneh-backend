from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from authentication.managers import UserManager
from validators import validate_image


class User(AbstractBaseUser, PermissionsMixin):
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
    is_private = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return "Username: {}, Email: {}".format(self.username, self.email)

    def get_full_name(self):
        return self.fullname

    def get_bio(self):
        return self.bio
