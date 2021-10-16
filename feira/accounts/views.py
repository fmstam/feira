from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .forms import BasicRegistrationForm, BasicAuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth import views
from django.contrib.messages.views import SuccessMessageMixin



class RegisterView(SuccessMessageMixin, CreateView):
    form_class = BasicRegistrationForm
    template_name = 'accounts/register.html'
    success_message = 'Registration is successful!, you can login now.'

    def get_success_url(self, **kwargs) -> str:
        """or using reverse_lazy"""
        #, args=(success_messages,)
        return reverse('home')


class LoginView(SuccessMessageMixin, views.LoginView):
    form_class = BasicAuthenticationForm
    template_name ='accounts/login.html'
    #success_message = 'You are logged-in!'

    # this is not necessary since we can
    #  set LOGIN_REDIRECT_URL = '/home' in setting.py
    # def get_success_url(self) -> str:
    #     return reverse('home')

    
