from django.urls import path
from django.urls.resolvers import URLPattern
from .views import ListingView

app_name ='fair'
urlpatterns =[
    path('listings', ListingView.as_view(), 'listings')

]