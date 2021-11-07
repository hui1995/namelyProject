from django.db import models
from django.db.models.fields import TextField
from django.db.models.fields.related import ForeignKey

from django.contrib.auth.models import AbstractUser

# Create your models here.
class CommentsModel(models.Model):
    content=TextField()
    user=ForeignKey(AbstractUser,on_delete=models.CASCADE)