from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .forms import BasicRegistrationForm
from django.views.generic import CreateView


class RegisterView(CreateView):
    
    registration_form = BasicRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

