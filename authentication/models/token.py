import binascii
import os

from django.db import models

from authentication.models import User


class Token(models.Model):
    """
    Athorization token model for reset password
    """

    key = models.CharField(max_length=6, primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='token')
    created_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(3)).decode()

    def __str__(self):
        return self.key
