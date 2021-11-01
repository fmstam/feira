## rest
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
# backend filters
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.filters import SearchFilter
# pagination
from rest_framework.pagination import LimitOffsetPagination

## auth stuff
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# caching
from django.core.cache import cache

# decorators
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

## http
from django.http import HttpResponseForbidden, response

## utils
from django.utils import timezone
from rest_framework.response import Response


# local stuff
from .serializers import ListingSerializer
from .models import Listing
from .serializers import ListingSerializer
from .views import OwnershipMixin


class ListingAPIPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class ListingAPIView(ListAPIView):

    """
    A typical API view class with filter, search, and pagination capabilities
    """
    # we can set the queryset or override get_queryset, 
    # see rest_framework.generics.GenericAPIView
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    # set filter backends and fields
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id', 'owner', 'slug') # it is the default too

    # searchable text fields 
    search_fields = ('title', 'description')

    # paginator
    pagination_class = ListingAPIPagination



class ListingCreateAPIView(LoginRequiredMixin, CreateAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()

    def post(self, request, *args, **kwargs):

        
        ## use chaching protect against flooding
        # a request is already in the cache?
        if cache.has_key('listing_created'):
            # request received but no listing was created
            return Response(status.HTTP_200_OK) 

        # otherwise, post the request and check if we need to store it
        response =  super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            # make a time gap of 300 ms to avoid db flooding
            cache.set('listing_created', True, timeout=300)
        return response


# one class for view, update, and delete
class ListingRetrieveUpdateDestroyAPIView(LoginRequiredMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    lookup_field = 'slug'

    def delete(self, request, *args, **kwargs):
        """
        Override the delete method.
        """
        listing_slug  = request.data.get('slug')
        response = super(ListingRetrieveUpdateDestroyAPIView, self).delete(request,
                                                                           *args, 
                                                                           **kwargs)
        # if request has succeeded, 
        # but that the client doesn't need to navigate away from its current page.
        if response.status_code == status.HTTP_204_NO_CONTENT:
            # remove the cached data
            cache.delete(f'listing_data_{listing_slug}')
        return response
    
 
    def update(self, request, *args, **kwargs):
        """
        Override the delete method.
        """
        # print(kwargs)
        response = super(ListingRetrieveUpdateDestroyAPIView, self).update(request, *args, **kwargs)
        # all good?
        if response.status_code == status.HTTP_200_OK:
            # update cache
            listing = response.data
            from django.core.cache import cache
            cache.set(f'listing_data_{listing["slug"]}',{
                'title': listing['title'],
                'description': listing['description'],
                'price' : listing['price'],
                'image': listing['image'],
                'modification_date': timezone.now()
            })
        return response





    













