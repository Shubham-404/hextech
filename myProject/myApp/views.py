from django.shortcuts import render
from .piechart import load_and_process_data, plot_1_hour
import os
from myApp.models import Signup
from myApp.models import Device

# Create your views here.

def home(request):
    # Provide the path to your CSV file (adjust the path as necessary)
    file_path = os.path.join(os.getcwd(), 'data', 'energy_data.csv')
    
    # Load and process the data
    data = load_and_process_data(file_path)
    
    # Generate the graph for the first available timestamp
    if not data.empty:
        time = data['Time'].iloc[0]
        graph_html = plot_1_hour(data, time)
    else:
        graph_html = "<p>No data available to generate the graph.</p>"
    
    # Pass the graph HTML to the template
    return render(request, 'myApp/home.html', {'graph_html': graph_html})


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


