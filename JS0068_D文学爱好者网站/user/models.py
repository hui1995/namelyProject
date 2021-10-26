from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pic=models.CharField(max_length=2048,default="image/default.png")
