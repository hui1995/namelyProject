from django.db import models

# Create your models here.

class GameModel(models.Model):
    sport=models.CharField(max_length=50)
    discipline = models.CharField(max_length=50)

class EventModel(models.Model):
    event = models.CharField(max_length=50,unique=True)
    gender=models.CharField(max_length=12)

class Medals(models.Model):
    city = models.CharField(max_length=50)
    year = models.IntegerField()
    gid=models.ForeignKey(GameModel,on_delete=models.CASCADE)
    eid=models.ForeignKey(EventModel,on_delete=models.CASCADE)
    athlete = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    country_code = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    medal = models.CharField(max_length=50)

