from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import Listing, ListingForm

# Create your views here.



class ListingView(SuccessMessageMixin, CreateView):
    form_class = ListingForm
    template_name = 'fair/listings.html'

    def get(self, request, *args, **kwrags):
        print('from the listingview get method')
        listings = Listing.objects.all()
        return render(request, 
                     self.template_name,
                     {'listings': listings})


    