from django.contrib import admin
from social.models.posts import Posts
from social.models import Board, BoardContains
# Register your models here.

admin.site.register(Posts)
admin.site.register(Board)
admin.site.register(BoardContains)