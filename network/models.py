from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone


class User(AbstractUser):
    pass


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, 
        related_name="poster")
    content = models.CharField(max_length=280)
    post_datetime = models.DateTimeField(default=timezone.now)
    edit_bool = models.BooleanField(default=False)
    edit_datetime = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        if self.edit_bool == False:
            # if post has original content, display this with original post datetime
            return f"{self.poster} posted:\n'{self.content}'\nat {self.post_datetime}"
        else:
            # if post was edited one or more times, display updated content with datetime of most recent edit
            return f"{self.poster} updated post to say:\n'{self.content}'\nat {self.edit_datetime}"

    def is_valid_post(self):
        return len(self.content) > 0 and len(self.content) <= 280


class Follows(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="following")
    active_bool = models.BooleanField(default=True)


class Likes(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="liker")
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
        related_name="liked_post")