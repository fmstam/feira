from django.urls import path
from django.urls.resolvers import URLPattern
from django.views.generic.base import TemplateView
from .views import ListingView

app_name ='fair'
urlpatterns =[
    path('', ListingView.as_view(), name='listings'),
    path('listings/', ListingView.as_view(), name='listings'),
    path('listings/<int:listing_id>', ListingView.as_view(), name='listings'),
    #path('<int:listing_id>/edit', ListingView.as_view(), name='listing')

]