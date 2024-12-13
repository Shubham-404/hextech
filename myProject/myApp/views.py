from django.shortcuts import render
from .piechart import load_and_process_data, plot_1_hour, plot_5_hours, plot_24_hours
import os
from datetime import timedelta  # Import timedelta
from myApp.models import Signup
from myApp.models import Device

# Create your views here

def home(request):
    file_path = os.path.join(os.getcwd(), 'data', 'energy_data.csv')
    
    # Load and process the data
    data = load_and_process_data(file_path)
    
    # Check if the data is available
    if data.empty:
        return render(request, 'myApp/home.html', {'graph_html_1': "<p>No data available.</p>", 'graph_html_2': "", 'graph_html_3': ""})
    
    # Generate the 1-hour graph for the first available timestamp
    time = data['Time'].iloc[0]
    graph_html_1 = plot_1_hour(data, time)
    
    # Generate the 5-hour graph for a time range
    start_time = time
    end_time = start_time + timedelta(hours=5)
    graph_html_2 = plot_5_hours(data, start_time, end_time)
    
    # Generate the 24-hour graph for a time range
    start_time_24 = data['Time'].min()
    end_time_24 = start_time_24 + timedelta(hours=24)
    graph_html_3 = plot_24_hours(data, start_time_24, end_time_24)
    
    # Pass the graphs to the template
    return render(request, 'myApp/home.html', {
        'graph_html_1': graph_html_1 or "<p>Unable to generate 1-hour graph.</p>",
        'graph_html_2': graph_html_2 or "<p>Unable to generate 5-hour graph.</p>",
        'graph_html_3': graph_html_3 or "<p>Unable to generate 24-hour graph.</p>"
    })


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


