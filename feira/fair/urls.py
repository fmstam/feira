from django.urls import path
from django.urls.resolvers import URLPattern
from django.views.generic.base import TemplateView
from .views import ListingView, ListingCreateView, ListingUpdateView, ListingDeleteView
from .helper import create_listings

app_name ='fair'
urlpatterns =[
    path('', ListingView.as_view(), name='listings'),
    path('random_listings', create_listings ),
    path('listings/', ListingView.as_view(), name='listings'),
    path('listings/user/<int:owner_id>', ListingView.as_view(), name='user_listings'),
    path('listings/cat/<slug:category_slug>', ListingView.as_view(), name='category_listings'),
    path('listings/<int:pk>', ListingView.as_view(), name='view_a_listing'),
    path('listings/<slug:listing_slug>', ListingView.as_view(), name='view_a_listing'),
    path('listings/new/', ListingCreateView.as_view(), name='create_a_listing'),
    path('listings/<int:pk>/edit', ListingUpdateView.as_view(), name='edit_a_listing'),
    path('listings/<int:pk>/delete', ListingDeleteView.as_view(), name='delete_a_listing')
    
]