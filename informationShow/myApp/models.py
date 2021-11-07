from django.db import models
from django.db.models.fields import DateField, TextField
from django.db.models.fields.related import ForeignKey

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    userType=models.IntegerField(default=0)
class CommentsModel(models.Model):
    content=TextField()
    createDate=DateField()
    user=ForeignKey(User,on_delete=models.CASCADE)