from django.contrib import admin
from social.models.posts import Posts
from social.models import Board, BoardContains, Like, Comment, Followers, Request
# Register your models here.

admin.site.register(Posts)
admin.site.register(Board)
admin.site.register(BoardContains)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Followers)
admin.site.register(Request)