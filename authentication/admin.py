from django.contrib import admin

from authentication.models import User, Token

admin.site.register(User)
admin.site.register(Token)
