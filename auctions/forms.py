from django.forms import ModelForm
from .models import Listing

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'img_url']
        labels = {
            'price': 'Minimum Bid (USD)',
            'img_url': 'Link to Image'
        }