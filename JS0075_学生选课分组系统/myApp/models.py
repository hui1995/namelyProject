from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


# class Admin(AbstractUser):
#     a_phone = models.CharField(max_length=64)
#     a_auth = models.IntegerField(default=1)  # 1是管理员,2是用户管理员，3权限管理员
#     a_sparce = models.CharField(max_length=64)
#     a_status = models.IntegerField(default=0)  # 1是管理员,2是用户管理员，3权限管理员



# class Auth(models.Model):
#     name = models.CharField(max_length=2048)


# class AuthRelationAdmin(models.Model):
#     admin_id = models.IntegerField()
#     auth_id = models.IntegerField()


# class Homeowner(models.Model):
#     h_house = models.CharField(max_length=2048)
#     h_name = models.CharField(max_length=2048)
#     h_id = models.CharField(max_length=2048)
#     h_phone = models.CharField(max_length=64)
#     h_cname = models.CharField(max_length=2048)
#     h_cphone = models.CharField(max_length=64)
#     h_password = models.CharField(max_length=2048)
#     h_sparce = models.CharField(max_length=2048)
#     s_avther=models.CharField(max_length=2048,default="/static/images/default.png")
# import datetime
# class Public(models.Model):
#     p_title=models.CharField(max_length=2048)
#     p_content=models.TextField()
#     p_time=models.DateTimeField(default=datetime.datetime.now())

# class Repair(models.Model):
#     r_place=models.CharField(max_length=2048)
#     r_name=models.CharField(max_length=2048)
#     r_phone=models.CharField(max_length=64)
#     r_status=models.CharField(max_length=64)
#     r_time=models.DateTimeField(default=datetime.datetime.now())

# class Complaints(models.Model):
#     h_account= models.ForeignKey('Homeowner',on_delete=models.CASCADE)
#     event=models.TextField()
#     c_time=models.DateTimeField(default=datetime.datetime.now())
#     c_status=models.CharField(max_length=64)

# class Guest(models.Model):
#     h_account= models.ForeignKey('Homeowner',on_delete=models.CASCADE)
#     g_phone=models.CharField(max_length=2048)
#     g_gname=models.CharField(max_length=2048)
#     g_gphone=models.CharField(max_length=2048)
#     g_time=models.DateTimeField(default=datetime.datetime.now())
#     g_status=models.CharField(max_length=64)

# class Report(models.Model):
#     h_account = models.ForeignKey('Homeowner',on_delete=models.CASCADE)
#     r_content=models.TextField()
#     time=models.DateTimeField(default=datetime.datetime.now())
#     status=models.CharField(max_length=64,default="未处理")
#     feedback=models.CharField(max_length=2048,default="",null=True,blank=True)

# class Staff(models.Model):
#     s_number=models.CharField(max_length=2048)
#     s_name=models.CharField(max_length=2048)
#     d_name=models.CharField(max_length=2048)
#     j_name=models.CharField(max_length=2048)
#     s_explan=models.CharField(max_length=2048)
#     s_id=models.CharField(max_length=26)
#     s_phone=models.CharField(max_length=64)
#     s_cname=models.CharField(max_length=64)
#     s_cphone=models.CharField(max_length=64)
