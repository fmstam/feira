from django.urls import path
from django.urls.resolvers import URLPattern
from django.views.generic.base import TemplateView
from .views import ListingView, ListingCreateView, ListingUpdateView, ListingDeleteView
from .helpers import create_listings
from .ML import SimilarityScorer

app_name ='fair'
urlpatterns =[
    
    # these are to populate the system
    path('random_listings/', create_listings ),
    path('calc_scores/', SimilarityScorer().add_all_similarities ),
    path('calc_features/', SimilarityScorer().calc_features, {'replace': True} ),
    path('update_scores/', SimilarityScorer().update_all_similarities ),

    # listing urls
    path('', ListingView.as_view(), name='listings'),
    path('listings/', ListingView.as_view(), name='listings'),
    path('listings/user/<int:owner_id>', ListingView.as_view(), name='user_listings'),
    path('listings/cat/<slug:category_slug>', ListingView.as_view(), name='category_listings'),
    path('listings/<int:pk>', ListingView.as_view(), name='view_a_listing'),
    path('listings/<slug:listing_slug>', ListingView.as_view(), name='view_a_listing'),
    path('listings/new/', ListingCreateView.as_view(), name='create_a_listing'),
    path('listings/<int:pk>/edit', ListingUpdateView.as_view(), name='edit_a_listing'),
    path('listings/<int:pk>/delete', ListingDeleteView.as_view(), name='delete_a_listing')



]