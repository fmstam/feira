from django import shortcuts
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import ListingForm
from .models import Listing
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, get_list_or_404



class OwnershipMixin():
    """
    A validation mixin to check the ownership of a listing when editing and deleting listings
    """

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != request.user:
            return HttpResponseForbidden()
        
        return super(OwnershipMixin, self).dispatch(request, *args, **kwargs)


# view class
class ListingView(CreateView):
    form_class = ListingForm
    
    def get_listing(self, filter, single=False):
        """
        Retrives listings based on the 'filter' or 404
        Returns the listing dictionary to be sent to the template
        """
        if single:
            listing = get_object_or_404(Listing, **filter)
            pks = listing.related_listing_1.values_list('listing_2', flat=True).order_by('-score')[:5]
            recommendations = Listing.objects.filter(pk__in=pks).all()
            listing_dict = {'listing': listing, 
                            'recommendations': recommendations
                            }
            template_name='fair/listing.html'
        else:
            if not filter: # all objects no filter
                listings =  Listing.objects.all()
            else: # muti-listing filter
                listings = get_list_or_404(Listing, **filter)
            
            listing_dict = {'active_listings': listings } 
            template_name='fair/listings.html'

        return template_name, listing_dict

       
    def get(self, request, *args, **kwargs):
        """
         Get listings based on the input arguments.
         it returns single or multiple listings depending on the input filter
         For example, looking up all listing of a given owner returns a list of listing
         while looking up a single listing by its pk returns a single listing
        """
        
        if kwargs: # any filters?
            # multiple listing filters
            if 'owner_id' in kwargs.keys():  # for a specific user
                template_name, listing_dict = self.get_listing({'owner': kwargs['owner_id']})

            # another filter could be
            # if category_id in kwargs.keys(): # for a given category
                # listing_dict = self.get_listing({'category': kwargs['category_id']})

            # single listing 
            elif 'pk' in kwargs.keys():  # a specific listing
                 template_name, listing_dict = self.get_listing({'pk': kwargs['pk']}, single=True)

        else: # all listings
            template_name, listing_dict = self.get_listing({}) # no filter

        self.template_name = template_name

        return render(request, 
                     template_name,
                     listing_dict
                     )


# create new class
class ListingCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = ListingForm
    template_name = 'fair/new_listing.html'
    success_message = "Listing is created successfully"
    
    def get_success_url(self, **kwargs) -> str:
        """instead of using reverse_lazy"""
        return reverse('home')
    
    def get_login_url(self) -> str:
        """
        Make sure the user is logged in
        """
        return reverse('accounts:login')

    def form_valid(self, form: ListingForm) -> HttpResponse:
        self.object = form.save(commit=False)
        self.object.owner = self.request.user # set the fk
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# edit class
class ListingUpdateView(SuccessMessageMixin, OwnershipMixin, LoginRequiredMixin, UpdateView):
    form_class = ListingForm
    model = Listing
    template_name = 'fair/new_listing.html'
    success_message = "Listing is updated successfully"

    def get_success_url(self, **kwargs) -> str:
        """instead of using reverse_lazy"""
        return reverse('home')

    def get_login_url(self) -> str:
        """
        Make sure the user is logged in
        """
        return reverse('accounts:login')

    def form_valid(self, form: ListingForm) -> HttpResponse:
        self.object = form.save(commit=False)
        self.object.owner = self.request.user # set the fk
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ListingDeleteView(SuccessMessageMixin, OwnershipMixin, LoginRequiredMixin, DeleteView):
    model = Listing
    success_message = "Listing is deleted successfully"

    def get_success_url(self, **kwargs) -> str:
        """instead of using reverse_lazy"""
        return reverse('home')

    def get_login_url(self) -> str:
        """
        Make sure the user is logged in
        """
        return reverse('accounts:login')