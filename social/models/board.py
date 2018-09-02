from django.db import models
from authentication.models import User


class Board(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    name = models.TextFieldField(max_length=20)

class BoardContains(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="board")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="board_contains")
