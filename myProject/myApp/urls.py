from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("insights/", views.insights, name = "insights"),
    path("devices/", views.devices, name = "devices"),
    path("join/", views.join, name = "join"),
    path("signup/", views.signup, name = "signup"),

]
