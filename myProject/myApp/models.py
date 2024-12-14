from django.db import models

# Create your models here.

class Device(models.Model):
    device_name= models.CharField(max_length=122)
    device_id= models.CharField(max_length=122)

class Signup(models.Model):
    username=models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    password=models.CharField(max_length=122)
