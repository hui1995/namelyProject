from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

from user.models import User




class Category(models.Model):
    name=models.CharField(max_length=2048,verbose_name="类名")
    def __str__(self):
        return self.name
    class Meta:
        # 末尾不加s
        verbose_name_plural = '分类'


class Book(models.Model):
    title=models.CharField(max_length=1024,verbose_name="标题")
    pic=models.ImageField(max_length=2048,verbose_name="封面",upload_to="static/image")
    detail=models.CharField(max_length=2048,verbose_name="详情")
    category=models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name="分类")
    content=models.TextField(verbose_name="简介")
    star=models.FloatField(verbose_name="评分")
    tags=models.CharField(max_length=2048,verbose_name="标签")
    create_time=models.DateField(verbose_name="创建时间")
    status=models.IntegerField(default=1,choices=((1,'上架'),(0,'下架')),verbose_name="状态")
    href=models.CharField(max_length=2048,verbose_name="链接")
    def __str__(self):
        return self.title

    class Meta:
        # 末尾不加s
        verbose_name_plural = '书籍'

# 书单
class CollectBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="用户")
    book = models.ForeignKey("Book", on_delete=models.CASCADE,verbose_name="书籍")
    content=models.TextField(verbose_name="评论内容")
    create_time=models.DateField(verbose_name="评论时间")

    class Meta:
        # 末尾不加s
        verbose_name_plural = '书评'

# 二级回复
class Comment2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    content=models.TextField()
    create_time=models.DateField()


class Article(models.Model):
    title=models.CharField(max_length=1024)
    content=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    create_time=models.DateTimeField()


class Message(models.Model):
    user = models.IntegerField()
    reply_user= models.ForeignKey(User, on_delete=models.CASCADE)
    content=models.TextField()
    create_time=models.DateTimeField()
