from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    sex = models.IntegerField(default=0) 
    birtday = models.DateTimeField() 
    summary = models.TextField() 
    type = models.IntegerField(default=0)  # 0是学生，1是教师
    grade=models.IntegerField()


class Course(models.Model):
    credit=models.IntegerField()
    score=models.FloatField()

    title=models.CharField(max_length=256)
    image=models.CharField(max_length=1024)
    summary=models.TextField()
    createDate=models.DateTimeField(auto_now=True)

class Theme(models.Model):
    name=models.CharField(max_length=256)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    
class GroupModel(models.Model):
    number=models.CharField(max_length=256)
    theme=models.ForeignKey(Theme,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    type=models.IntegerField(default=0)

class CourseDetail(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
class CourseStudent(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
