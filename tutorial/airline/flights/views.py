from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Flight, Passenger

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
        "passengers": passengers,
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })

def book(request:HttpRequest, flight_id:int):
    
    if request.method == "POST":
        try:
            flight = Flight.objects.get(pk=flight_id)
            passenger_id = int(request.POST["passenger"])
            passenger = Passenger.objects.get(pk=passenger_id)
            passenger.flights.add(flight)
        except Flight.DoesNotExist:
            flight = None
        except Passenger.DoesNotExist:
            passenger = None

    args = flight.id if flight else None
    return HttpResponseRedirect(reverse("flight", args=(args,)))

