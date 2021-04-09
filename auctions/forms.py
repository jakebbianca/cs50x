from django.forms import ModelForm, URLInput, Select
from django.utils.translation import gettext_lazy as _
from .models import Listing, Bid


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'img_url', 'category']
        labels = {
            'price': _("Minimum Bid (USD)"),
            'img_url': _("Link to Image"),
        }
        widgets = {
            'img_url': URLInput(attrs={'placeholder': "https://"})
        }
        error_messages = {
            'title': {
                'max_length': _("Title length may not exceed 100 characters.")
            },
            'description': {
                'max_length': _("Description length may not exceed 2000 characters.")
            },
            'price': {
                'max_digits': _("Maximum price allowed is $9,999,999,999.99."),
                'decimal_places': _("Price must include exactly two digits for whole cents (USD).")
            }
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']
        labels = {
            'bid': _("Place a bid on this item:"),
        }
        help_texts = {
            'bid': _("Enter a $ amount.")
        }
        error_messages = {
            'bid': {
                'max_digits': _("Maximum bid allowed is $9,999,999,999.99."),
                'decimal_places': _("Price must include exactly two digits for whole cents (USD).")
            }
        }