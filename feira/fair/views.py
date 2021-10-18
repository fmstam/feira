from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import Listing, ListingForm

# Create your views here.



class ListingView(SuccessMessageMixin, CreateView):
    class_form = ListingForm
    template_name = 'listings.html'

    