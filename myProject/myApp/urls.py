from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("insights/", views.insights, name = "insights"),
    path("devices/", views.devices, name = "devices"),
    path('join/', views.join, name='join'),
    path("signup/", views.signup, name = "signup"),
    path('logout/', views.logout_view, name='logout'),   
    path('live_data/', views.live_data, name='live_data'),
]
