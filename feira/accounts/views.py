from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .forms import BasicRegistrationForm, BasicAuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth import views
from django.contrib.messages.views import SuccessMessageMixin



class RegisterView(SuccessMessageMixin, CreateView):
    """
    User registration view.
    See BasicRegistrationForm for details.
    """
    form_class = BasicRegistrationForm
    template_name = 'accounts/register.html'
    success_message = 'Registration is successful!, you can login now.'

    def get_success_url(self, **kwargs) -> str:
        """or using reverse_lazy"""
        return reverse('home')


class LoginView(SuccessMessageMixin, views.LoginView):
    """
     Typical login view.
     If successes, then the user will be redirected to the LOGIN_REDIRECT_URL in the setting.py
    """
    form_class = BasicAuthenticationForm
    template_name ='accounts/login.html'
    

    
