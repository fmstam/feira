from django.shortcuts import render
from django.urls import reverse
from .forms import BasicRegistrationForm
from django.views.generic import CreateView


class RegisterView(CreateView):
    
    registration_form = BasicRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse('fair:index')

