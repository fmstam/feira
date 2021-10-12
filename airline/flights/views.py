from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from .models import Flight

# Create your views here.

def index(request:HttpRequest):
    return render(request, "flights/index.html",{
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    """ Get a flight given its flight id
    """
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        flight = None

    if flight:
        passengers =  flight.passengers.all()
    return render(request, "flights/flights.html",{
        "flight": flight,
        "passengers": passengers
    })
