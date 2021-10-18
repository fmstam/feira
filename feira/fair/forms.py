
from operator import imod
from django import forms

from django import forms
from django.forms import fields

from .models import Listing


class ListingForm(forms.ModelForm):
    "Allow user to add a new listing"

    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'image']

    
