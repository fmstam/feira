from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls.resolvers import URLPattern
from django.views.generic.base import TemplateView

# views
from .views import  ListingView, ListingCreateView, ListingUpdateView, ListingDeleteView, DashboardView
from .api_views import ListingAPIView, ListingCreateAPIView, ListingRetrieveUpdateDestroyAPIView, \
                        ProgressCallBackAPIView, DashboardAPIView

# helpers and ML
from .helpers import create_listings, fix_slugs
from .ML import FeatureExtractor

app_name ='fair'
urlpatterns =[
    # ML and db views
    path('random_listings/', create_listings ),
    path('fix_slugs/', fix_slugs ),
    # path('calc_scores/', SimilarityScorer().add_all_similarities ),
    path('dash/', DashboardView.as_view() , name="dash" ),
    
    # path('update_scores/', SimilarityScorer().update_all_similarities ),

    # typical views
    path('', ListingView.as_view(), name='listings'),
    path('listings/', ListingView.as_view(), name='listings'),
    path('listings/user/<int:owner_id>', ListingView.as_view(), name='user_listings'),
    path('listings/cat/<slug:category_slug>', ListingView.as_view(), name='category_listings'),
    # path('listings/<int:pk>', ListingView.as_view(), name='view_a_listing'),
    path('listings/<slug:slug>', ListingView.as_view(), name='view_a_listing'),
    path('listings/new/', ListingCreateView.as_view(), name='create_a_listing'),
    path('listings/<slug:slug>/edit', ListingUpdateView.as_view(), name='edit_a_listing'),
    path('listings/<slug:slug>/delete', ListingDeleteView.as_view(), name='delete_a_listing'),

    # API views
    path('api/v1/listings/', ListingAPIView.as_view(), name='api_listing'),
    path('api/v1/listings/new/', ListingCreateAPIView.as_view(), name='api_create_a_listing'),
    path('api/v1/listings/<slug:slug>/', ListingRetrieveUpdateDestroyAPIView.as_view(), name='api_rud_a_listing'),
    path('api/v1/dash/', DashboardAPIView.as_view() , name="api_dash" ),
    path('api/v1/dashprogress/<str:acf_task_id>/', ProgressCallBackAPIView.as_view() , name="api_dashprogress" ),
    path('api/v1/dashprogress/', ProgressCallBackAPIView.as_view() , name="api_dashprogress" ),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)