from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone


class User(AbstractUser):
    pass
    #followers? -- needed or just count from Follows class?


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    content = models.CharField(max_length=280)
    post_datetime = models.DateTimeField(default=timezone.now)
    edit_bool = models.BooleanField(default=False)
    edit_datetime = models.DateTimeField(default=None)

class Follows(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    active_bool = models.BooleanField(default=True)

class Likes(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liker")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")