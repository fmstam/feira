## rest
from os import replace
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
from .ML import ml_calc_features, ml_calc_scores

# celery 
from celery.result import AsyncResult
from celery.states import state, PENDING, SUCCESS, STARTED


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
    task_execution_map ={ 
        # tasks, will be moved to a config file or db
        'ACF': {'method': ml_calc_features, 
                'callback-end-point': 'fair:api_dashprogress',
                'timeout': 1000 # estimated from the task progress speed.
                },

        'CLS': {'method': ml_calc_scores, 
                'callback-end-point': 'fair:api_dashprogress',
                'timeout': 1000 # estimated from the task progress speed.
                },
        
        'CDL': {'method': ml_calc_features, 
                'callback-end-point': 'fair:api_dashprogress',
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
        ## TODO: check if user is allowed to access it.
        # only admin can access it will need to use permissions here

        def create_task(method, task_name, clean_slate=False):
            """
            Create a task, cache it, and return its id
            """
            # clean-slate?
            if cache.has_key(task_name) and clean_slate:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            # all good, create a new task and cache it
            task = method.delay()
            task_id = task.id
            cache.set(task_name, {
                        'task_id':task_id
                    })
            return task_id
            
        serializer = self.get_serializer(data=request.data)
        #serializer.to_internal_value(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # release data from the serializer to update it
        data = serializer.data

        # lookup the task method
        method =  self.task_execution_map[data['task_name']]['method']
         # not cached, create it
        if not cache.has_key(data['task_name']):
            task_id = create_task(method, data['task_name'], clean_slate=True)
        else: # already in the cache
            task_id = cache.get(data['task_name'])['task_id']
            # check it is status
            task_results = AsyncResult(task_id)
            
            # check if it is zombi task
            if not task_results or task_results.state >= state(SUCCESS): 
                # TODO: NEED TO DELETE ANY EXISTING BEFORE CREATION

                # then create a new one
                task_id = create_task(method, data['task_name'])

        # attach task_id to the response data
        data['task_id'] = task_id
        # attach the task progress listener end-point
        data['callback-end-point'] = reverse(self.task_execution_map[data['task_name']]['callback-end-point'])
        # attach the timeout
        data['timeout'] = self.task_execution_map[data['task_name']]['timeout']

        # return response
        return Response(data=data, status=status.HTTP_201_CREATED)
        


class ProgressCallBackAPIView(LoginRequiredMixin, ListAPIView):
        """
            This is the end-point that used by the frontend to get the current progress 
            of celery backend tasks.
        """

        def get(self, request, *args, **kwargs):
            """
            Typical GET handler
            """
            ## TODO: check if user is allowed to access it.
            # only admin can access it will need to use permissions here

            ## check if task already has an id
    
            result = AsyncResult(kwargs['acf_task_id'])
            response_data = {
                'state': result.state,
                'details': result.info, # the progress is here, see 
            }
            # if not finished yet
            if response_data['state'] != state(SUCCESS):
                # pending or started   
                if (response_data['state'] == state(PENDING)) or (response_data['state'] == state(STARTED)):
                    response_data['details']['current'] = 0
            return response.HttpResponse(json.dumps(response_data), content_type='application/json')