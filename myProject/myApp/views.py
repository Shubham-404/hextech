from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

logged = True;
def home(request) : 
    if(logged):
        return render(request, "myApp/home.html")
    else:
        return render(request, "myApp/join.html")
        

def insights(request):
    return render(request, "myApp/insights.html")

def devices(request):
    return render(request, "myApp/devices.html")

def join(request):
    return render(request, "myApp/join.html")

