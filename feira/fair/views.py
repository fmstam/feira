from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import ListingForm
from .models import Listing
from django.urls import reverse


class ListingView(CreateView):
    form_class = ListingForm
    template_name = 'fair/listings.html'

    def get(self, request, *args, **kwargs):
        if kwargs:
            # filter them
            if kwargs['owner_id']:
               listings = Listing.objects.filter(owner=kwargs['owner_id'])
        else:
            listings =  Listing.objects.all()
        return render(request, 
                     self.template_name,
                     {'active_listings': listings }
                     )


class ListingCreateView(CreateView):
    form_class = ListingForm
    template_name = 'fair/new_listing.html'

    def get_success_url(self, **kwargs) -> str:
        """instead of using reverse_lazy"""
        return reverse('home')

    def form_valid(self, form: ListingForm) -> HttpResponse:
        self.object = form.save(commit=False)
        self.object.owner = self.request.user # set the fk
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())