from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .forms import BasicRegistrationForm
from django.views.generic import CreateView

class RegisterView(CreateView):
    form_class = BasicRegistrationForm
    template_name = 'accounts/register.html'
    


    
    def get_success_url(self, **kwargs):
        """or using reverse_lazy"""
        success_messages = ['Registration is successful!, you can login now.']
        return reverse('home', args=(success_messages,))

