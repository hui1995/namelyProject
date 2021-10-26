from django.db import models
# Create your models here.

import datetime
class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)
    lock_time=models.DateField(null=True,blank=True)
    count1=models.IntegerField(default=0)
    count2=models.IntegerField(default=0)

    class Meta:
        ordering = ["c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"

class Campus(models.Model):
    name=models.CharField(max_length=264)
    def __str__(self):
        return self.name

class Teachingbuilding(models.Model):
    name=models.CharField(max_length=264)
    def __str__(self):
        return self.name

class Foor(models.Model):
    teachingbuilding = models.ForeignKey('Teachingbuilding',on_delete=models.CASCADE)
    campus = models.ForeignKey('Campus',on_delete=models.CASCADE)
    name=models.CharField(max_length=264)
    def __str__(self):
        return self.name

class ClassRoom(models.Model):
    name=models.CharField(max_length=264)
    foor = models.ForeignKey('Foor',on_delete=models.CASCADE)
    def __str__(self):
        return self.name



class Seat(models.Model):

    classRoom = models.ForeignKey('ClassRoom',on_delete=models.CASCADE)
    name=models.CharField(max_length=264)
    status=models.IntegerField(default=0)
    def __str__(self):
        return self.name
import datetime
class AppointmentRecord(models.Model):
    seat = models.ForeignKey('Seat',on_delete=models.CASCADE)
    appoint_date=models.DateField(default=datetime.datetime.now())
    user_id=models.ForeignKey("User",on_delete=models.CASCADE)
    appoint_date_hour=models.DateTimeField(default=datetime.datetime.now())
    appoint_type=models.IntegerField(default=0)#0预测成功，1签到，2签离，3未签到，4未签离，5取消预约
    status=models.IntegerField(default=0)




