from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    #followers? -- needed or just count from Follows class?


#will need model form to create new post
#class Post(models.Model):
    #id (auto)
    #poster FOREIGN KEY user -- maybe call user instead?
    #content
    #date
    #time
    #datetime?
    #likes? -- needed or will this pull from Likes class?

#class Follows:
    #id (auto)
    #follower FOREIGN KEY user
    #following FOREIGN KEY user
    #active? -- instead of deleting row, just set this to 0/inactive when someone unfollows

#class Likes:
    #id (auto)
    #user FOREIGN KEY
    #post FOREIGN KEY


