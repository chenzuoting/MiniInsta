from django.contrib import admin

from Insta.models import InstaUser, Post, UserConnection, Like

# Register your models here.

admin.site.register(InstaUser)
admin.site.register(Post)
admin.site.register(UserConnection)
admin.site.register(Like)