from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    phone = models.CharField(max_length=64)
    name = models.CharField(max_length=2048)


