from django.shortcuts import render
from django.http import HttpResponse
from myApp.models import Signup
from myApp.models import Device

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
    if request.method=="POST":
        device_name=request.POST.get('device_name')
        device_id=request.POST.get('device_id')
        devices=Device(device_name=device_name,device_id=device_id)
        devices.save()
    return render(request, "myApp/devices.html")

def join(request):
    return render(request, "myApp/join.html")

def signup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        signup=Signup(username=username,email=email,password=password,)

        signup.save()
    return render(request, "myApp/signup.html")


