from django.db import models
from authentication.models import User

# Create your models here.

class Followers(models.Model):
  """
  This model use for followers and following for users.
  """

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  following = models.ForeignKey(User, on_delete=models.CASCADE)
