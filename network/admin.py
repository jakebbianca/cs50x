from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Follows, Likes

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User

admin.site.register(User, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Follows)
admin.site.register(Likes)