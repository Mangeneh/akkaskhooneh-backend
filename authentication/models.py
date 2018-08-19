from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    fullname = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True, null=True)
    phone_number = models.CharField(max_length=30, unique=True, blank=True, null=True)
    register_date = models.DateField(auto_now=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return "Username: {}, Email: {}".format(self.username, self.email)
