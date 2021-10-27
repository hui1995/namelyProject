from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class Dept(models.Model):
    no = models.CharField(max_length=64, verbose_name="部门编号")
    name = models.CharField(max_length=2048)

    def __str__(self):
        return self.no


class User(AbstractUser):
    phone = models.CharField(max_length=64)
    name = models.CharField(max_length=2048)
    deptId = models.ForeignKey(Dept, null=True, on_delete=models.CASCADE)
    role = models.IntegerField(default=0)  # 0部门公车管理员，1是部门领导，2是副主管，3，是主管


import datetime


class Car(models.Model):
    no = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    nums = models.IntegerField()
    knmus = models.CharField(max_length=64)
    address = models.CharField(max_length=2048)
    status = models.CharField(max_length=64)
    dept=models.ForeignKey(Dept,on_delete=models.CASCADE)


class CarLog(models.Model):
    option_type = models.CharField(max_length=64)
    remark = models.CharField(max_length=2048)
    create_time = models.DateTimeField(default=datetime.datetime.now())
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)


class CarApply(models.Model):
    dept=models.ForeignKey(Dept,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    basis = models.CharField(max_length=2048, verbose_name="申请依据")
    place = models.CharField(max_length=2048, verbose_name="申请地点")
    cause = models.CharField(max_length=2048, verbose_name="申请事由")
    desti = models.CharField(max_length=2048, verbose_name="申请目的地")
    penum = models.IntegerField(verbose_name="申请人数")
    usetime = models.DateTimeField(verbose_name="申请使用时间")
    gettime = models.DateTimeField(verbose_name="驱车时间")
    flow_rank = models.IntegerField(verbose_name="审核流等级")
    flow_id=models.IntegerField(default=0)
    status = models.CharField(verbose_name="申请状态", max_length=64)
    create_time = models.DateTimeField(verbose_name="创建时间", default=datetime.datetime.now())


class CarApplyLink(models.Model):
    applyId = models.ForeignKey(CarApply, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=64)
    remark = models.CharField(max_length=2048,null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", default=datetime.datetime.now())
    update_time = models.DateTimeField(verbose_name="更新时间", default=datetime.datetime.now())
