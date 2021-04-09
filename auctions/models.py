from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator, MinLengthValidator
from decimal import Decimal


class User(AbstractUser):
    pass

# Create Listing: Users should be able to visit a page to create a new listing.
# They should be able to specify a title for the listing, a text-based description, and what the starting bid should be.
# Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
class Listing(models.Model):
    CF = 'CF'
    BOOKS = 'BOOKS'
    MMG = 'MMG'
    ELEC = 'ELEC'
    COMP = 'COMP'
    SMART = 'SMART'
    HGT = 'HGT'
    PET = 'PET'
    FG = 'FG'
    BH = 'BH'
    TKB = 'TKB'
    HAND = 'HAND'
    SPORTS = 'SPORTS'
    OUT = 'OUT'
    AUTOIND = 'AUTOIND'
    OTHER = 'OTHER'
    CATEGORIES = [
        (CF, 'Clothing/Fashion'), (BOOKS, 'Books'), (MMG, 'Movies, Music, & Games'),
        (ELEC, 'Electronics'), (COMP, 'Computers'), (SMART, 'Smart Home'), (HGT, 'Home, Garden, & Tools'),
        (PET, 'Pet Supplies'), (FG, 'Food & Grocery'), (BH, 'Beauty & Health'),  
        (TKB, 'Toys, Kids, & Baby'), (HAND, 'Handmade'), (SPORTS, 'Sports'),
        (OUT, 'Outdoors'), (AUTOIND, 'Automotive & Industrial'), (OTHER, 'Other')
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"), "Bids must be placed for a minimum of $0.01.")])
    img_url = models.URLField(max_length=200, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORIES, default=CF)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mylisting')
    status = models.BooleanField(default=True)



