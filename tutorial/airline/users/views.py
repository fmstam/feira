from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def index(request:HttpRequest)-> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

def login(request:HttpRequest)-> HttpResponse:
    return render(request, "users/login.html")

def logout(request:HttpRequest)-> HttpResponse:
    pass