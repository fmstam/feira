from django.urls import path
from django.urls.resolvers import URLPattern
from django.views.generic.base import TemplateView
from .views import ListingView, ListingCreateView

app_name ='fair'
urlpatterns =[
    path('', ListingView.as_view(), name='listings'),
    path('listings/', ListingView.as_view(), name='listings'),
    path('listings/user/<int:owner_id>', ListingView.as_view(), name='listings'),
    path('listings/view/<int:listing_id>', ListingView.as_view(), name='listings'),
    path('listings/edit/<int:listing_id>', ListingView.as_view(), name='listing'),
    path('listings/new/', ListingCreateView.as_view(), name='create_listings')
]