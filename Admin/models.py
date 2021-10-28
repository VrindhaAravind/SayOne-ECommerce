from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Staff(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)