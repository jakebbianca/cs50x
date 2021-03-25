from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class User(AbstractUser):
    pass

# Create Listing: Users should be able to visit a page to create a new listing.
# They should be able to specify a title for the listing, a text-based description, and what the starting bid should be.
# Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    img_url = models.URLField(max_length=200, blank=True)
    category = models.CharField(max_length=100)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mylisting')
    status = models.BooleanField(default=True)



