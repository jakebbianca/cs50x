from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.urls import reverse


class User(AbstractUser):
    
    def serialize(self):
        return {
            "user_id": self.id,
            "username": self.username,
            "followers": Follows.objects.filter(following=self, active_bool=True).count(),
            "following": Follows.objects.filter(follower=self, active_bool=True).count()
        }

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

    def serialize(self):
        
        if self.edit_datetime is not None:
            self.edit_datetime = self.edit_datetime.strftime("%b %d %Y, %I:%M %p")

        return {
            "post": self.id,
            "poster_id": self.poster.id,
            "poster_username": self.poster.username,
            "content": self.content,
            "post_datetime": self.post_datetime.strftime("%b %d %Y, %I:%M %p"),
            "edit_bool": self.edit_bool,
            "edit_datetime": self.edit_datetime,
            "poster_url": reverse('profile', kwargs={'user_id': self.poster.id}),
            "likes": Likes.objects.filter(post=self, active_bool=True).count()
        }

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
    active_bool = models.BooleanField(default=True)