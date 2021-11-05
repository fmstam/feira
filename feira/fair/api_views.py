## rest
from django.urls.base import reverse
from rest_framework.generics import views, ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import serializers, status
from rest_framework.permissions import DjangoObjectPermissions
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
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser



# local stuff
from .models import Listing
from .serializers import ListingSerializer, TaskSerializer
from .views import OwnershipMixin
from .ML import ml_calc_features


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
 
        ## use caching protect against flooding
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
    serializer_class = TaskSerializer
    queryset = Listing.objects.all()
    permission_classes = [DjangoObjectPermissions] # with dj-guardina backend
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




class DashboardAPIView(LoginRequiredMixin, CreateAPIView):
    serializer_class = TaskSerializer
    task_execution_map ={ # tasks, will be moved to a config file or db
        'ACF': {'method': ml_calc_features, 
                'callback-end-point': 'fair:calc_features',
                'timeout': 1000 # estimated from the task progress speed.
                }
    }
    
    def create(self, request, *args, **kwargs):
        """
        Get the request from the client and create a task.
        Each task will have an executor (Celery task) and a callback.
        The client will call the callback to fetch the current progress of 
        the task.
        """
        serializer = self.get_serializer(data=request.data)
        #serializer.to_internal_value(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # release data from the serializer to update it
        data = serializer.data
        
       

        # lookup the task method
        method =  self.task_execution_map[data['task_name']]['method']
         # cache checkup
        if not cache.has_key(data['task_name']):
            task = method.delay()
            task_id = task.id
            cache.set(data['task_name'], {
                        'task_id':task_id
                    })
        else: # already in the cache, return the cached task
            task_id = cache.get(data['task_name'])['task_id']
            
        # attach task_id to the response data
        data['task_id'] = task_id
        # attach the task progress listener end-point
        data['callback-end-point'] = reverse(self.task_execution_map[data['task_name']]['callback-end-point'])
        # attach the timeout
        data['timeout'] = self.task_execution_map[data['task_name']]['timeout']

        # return response
        return Response(data=data, status=status.HTTP_201_CREATED)
        
    # def post(self, request, *args, **kwargs):
        
    #     if request.data['method'] == 'ACF':
    #         # check if we have already a cached running task
    #         # if cache.has_key('ACF'):
    #         #     return Response(status.HTTP_200_OK)

    #         # else start the task
    #         task = ml_calc_features.delay()
    #         # cache it
    #         cache.set('ACF', {
    #             'task_id':task.task_id
    #         })
    #         # get response
    #     response = super(views.APIView, self).post(request, *args, **kwargs)

    #     return response
          