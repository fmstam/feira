from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls.resolvers import URLPattern
from django.views.generic.base import TemplateView

# views
from .views import ListingView, ListingCreateView, ListingUpdateView, ListingDeleteView
from .api_views import ListingAPIView, ListingCreateAPIView, ListingRetrieveUpdateDestroyAPIView

# helpers and ML
from .helpers import create_listings
from .ML import SimilarityScorer

app_name ='fair'
urlpatterns =[
    
    
    # ML views
    path('random_listings/', create_listings ),
    path('calc_scores/', SimilarityScorer().add_all_similarities ),
    path('calc_features/', SimilarityScorer().calc_features, {'replace': False} ),
    path('update_scores/', SimilarityScorer().update_all_similarities ),

    # typical views
    path('', ListingView.as_view(), name='listings'),
    path('listings/', ListingView.as_view(), name='listings'),
    path('listings/user/<int:owner_id>', ListingView.as_view(), name='user_listings'),
    path('listings/cat/<slug:category_slug>', ListingView.as_view(), name='category_listings'),
    path('listings/<int:pk>', ListingView.as_view(), name='view_a_listing'),
    path('listings/<slug:listing_slug>', ListingView.as_view(), name='view_a_listing'),
    path('listings/new/', ListingCreateView.as_view(), name='create_a_listing'),
    path('listings/<int:pk>/edit', ListingUpdateView.as_view(), name='edit_a_listing'),
    path('listings/<int:pk>/delete', ListingDeleteView.as_view(), name='delete_a_listing'),

    # API views
    path('api/listings/', ListingAPIView.as_view(), name='api_listing'),
    path('api/listings/new/', ListingCreateAPIView.as_view(), name='api_create_a_listing'),
    path('api/listings/<int:id>/', ListingRetrieveUpdateDestroyAPIView.as_view(), name='api__a_listing'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)