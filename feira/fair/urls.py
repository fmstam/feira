from django.urls import path
from django.urls.resolvers import URLPattern
from django.views.generic.base import TemplateView

app_name ='fair'
urlpatterns =[
    path('', TemplateView.as_view(), 'index')

]