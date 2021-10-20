
from operator import imod
from django import forms

from django import forms
from django.forms import fields

from .models import Listing


class ListingForm(forms.ModelForm):
    "Allow user to add a new listing"

    ## frontend constraints

    # price is positive value, see the model for the backend constraint
    price = forms.DecimalField(required=True, max_digits=6, min_value=0)

    class Meta:
        model = Listing
        fields = ['title', 'price', 'category', 'description', 'image']

    
