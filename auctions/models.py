from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Create Listing: Users should be able to visit a page to create a new listing.
# They should be able to specify a title for the listing, a text-based description, and what the starting bid should be.
# Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField
    min_bid = models.DecimalField(decimal_places=2)
    img_url = models.URLField()
