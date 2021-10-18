from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import Listing, ListingForm


class ListingView(SuccessMessageMixin, CreateView):
    form_class = ListingForm
    template_name = 'fair/listings.html'

    def get(self, request, *args, **kwargs):
        print(*args)
        return render(request, 
                     self.template_name,
                     {'active_listings': Listing.objects.all()}
                     )


    