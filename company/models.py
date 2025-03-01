from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=50, null=True)
    phone = models.CharField()
    gst_number = models.CharField()
    address = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)