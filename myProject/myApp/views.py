from django.shortcuts import render, redirect   
from .piechart import load_and_process_data, plot_1_hour, plot_5_hours, plot_24_hours
import os, random
from django.http import JsonResponse
from datetime import timedelta  # Import timedelta
from myApp.models import Device
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate

# Create your views here
last_data = {
    "Fridge": 2.5,
    "AC": 3.0,
    "TV": 1.0,
}

def live_data(request):
    global last_data

    data = {}
    for appliance, last_value in last_data.items():
        if appliance == "Fridge":
            variation = random.uniform(-0.1, 0.1)
            new_value = max(1.5, min(3.5, last_value + variation))
        elif appliance == "AC":
            time_of_day = random.uniform(0, 24)
            baseline = 4.0 if 12 <= time_of_day <= 18 else 2.0
            variation = random.uniform(-0.5, 0.5)
            new_value = max(1.5, min(5.0, baseline + variation))
        elif appliance == "TV":
            active = random.choice([True, False])
            new_value = random.uniform(0.5, 2.0) if active else 0.0

        data[appliance] = round(new_value, 2)
        last_data[appliance] = new_value

    tips = []
    if data["AC"] > 4.0:
        tips.append("Consider increasing the temperature setting on your AC.")
    if data["Fridge"] > 3.0:
        tips.append("Check if the fridge door is sealed properly.")
    if data["TV"] > 1.5:
        tips.append("Reduce screen brightness to save energy.")

    return JsonResponse({"Fridge": data["Fridge"], "AC": data["AC"], "TV": data["TV"], "Tips": tips})


def energy_tips(data):
    tips = []
    if data['AC'] > 3:
        tips.append("Reduce AC usage or switch to eco mode.")
    if data['Fridge'] > 2:
        tips.append("Ensure the fridge door is sealed properly.")
    if data['TV'] > 1:
        tips.append("Turn off the TV when not in use.")
    return tips

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
    if request.user.is_authenticated:
        return redirect('/')  # Redirect to home if user is already logged in
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('/')  # Replace 'home' with your desired redirect page
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "myApp/join.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home if user is already logged in
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        if password == password_confirm:
            try:
                # Create a new user using Django's built-in User model
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Account created successfully')
                return redirect('login')  # Redirect to login page after signup
            except Exception as e:
                messages.error(request, f"Error creating account: {e}")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "myApp/signup.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('/')  # Replace 'home' with your desired redirect page
