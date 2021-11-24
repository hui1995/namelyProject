from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    userType = models.IntegerField(default=0) #0:买家，1卖家，2管理员
    money=models.DecimalField(max_digits=10, decimal_places=2, verbose_name="余额")

class CashOutRecord(models.Model):
    createDate=models.DateTimeField(auto_now=True)
    type = models.IntegerField()#提现类型
    money=models.DecimalField(max_digits=10, decimal_places=2, verbose_name="提现金额")
