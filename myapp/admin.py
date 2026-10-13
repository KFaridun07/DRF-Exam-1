from django.contrib import admin
from .models import User, Profile, Post, Like, Favorite

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Favorite)

# Register your models here.
