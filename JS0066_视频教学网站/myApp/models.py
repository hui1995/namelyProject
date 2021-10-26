from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    status = models.IntegerField(default=2)

class Message(models.Model):
    content=models.TextField()
    teacherId=models.IntegerField()
    stu=models.ForeignKey(User,on_delete=models.CASCADE)
    create_time=models.DateTimeField()

class Message2(models.Model):

    message=models.ForeignKey(Message,on_delete=models.CASCADE)
    replay=models.TextField(null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    replay_time=models.DateTimeField(null=True)

class Video(models.Model):
    teacher=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=2048)
    pic=models.CharField(max_length=2048)
    video=models.CharField(max_length=2048)
    create_time=models.DateTimeField()

class FileInfo(models.Model):
    file=models.CharField(max_length=2048)
    title=models.CharField(max_length=2048)
    video=models.ForeignKey(Video,on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="教师")
    video = models.ForeignKey(Video, on_delete=models.CASCADE,verbose_name="视频")
    content=models.TextField(verbose_name="评论内容")
    create_time=models.DateField(verbose_name="评论时间")

    class Meta:
        # 末尾不加s
        verbose_name_plural = '评论'

# 二级回复
class Comment2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    content=models.TextField()
    create_time=models.DateField()


