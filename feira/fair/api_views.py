from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter



from .serializers import ListingSerializer
from .models import Listing
from .serializers import ListingSerializer



class ListingAPIView(ListAPIView):

    # we can set the queryset or override get_queryset, 
    # see rest_framework.generics.GenericAPIView
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    # set filter backends and fields
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id', 'owner', 'slug') # it is the default too

    # searchable text fields 
    search_fields = ('title', 'description')






