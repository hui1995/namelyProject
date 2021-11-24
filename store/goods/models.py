from django.db import models

# Create your models here.

from user.models import User


class Category(models.Model):
    name = models.CharField(verbose_name="类别名", max_length=50)
class Goods(models.Model):
    name = models.CharField(max_length=2048, verbose_name="标题")
    size = models.CharField(max_length=64, verbose_name="规格")
    type = models.ForeignKey(Category,on_delete=models.CASCADE)
    usertype = models.ForeignKey(User,on_delete=models.CASCADE)#卖家
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    stock = models.IntegerField(verbose_name="库存")
    sold = models.IntegerField(verbose_name="已售", default=0, null=True, blank=True)
    publish_date = models.DateField(verbose_name="发布时间", )
    goods_image = models.ImageField(verbose_name="商品主图", upload_to='static/image')
    goods_detail_iamge = models.ImageField(verbose_name="商品细节图片", upload_to='static/image')
    content = models.TextField(verbose_name="文字描述")
    collect = models.IntegerField(verbose_name="收藏",default=0,null=True,blank=True)
    expressFee= models.DecimalField(max_digits=10, decimal_places=2, verbose_name="配送费")

    def __str__(self):
        return self.name

class CollectGoods(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey("Goods", on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey("Goods", on_delete=models.CASCADE)
    num = models.IntegerField(default=1)


class Address(models.Model):
    username = models.CharField(max_length=2048)
    phone = models.CharField(max_length=2048)
    address = models.CharField(max_length=2048)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.address + "-" + self.phone


class Order(models.Model):
    status = models.IntegerField(default=0)#choices=((0,'待发货'),(1,'代发货'),(2,'代付款'),(3,'已发货')(4,'签收'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey("Address", on_delete=models.CASCADE)
    total_price=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    def __str__(self):
        return str(self.id)


class OrderDetail(models.Model):
    goods = models.ForeignKey("Goods", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    num=models.IntegerField(default=1)


