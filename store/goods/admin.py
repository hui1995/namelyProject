from django.contrib import admin
from goods.models import Goods,Order,OrderDetail
# Register your models here.

class GoodsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','address','total_price','status')

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('id','goods','order','price')


admin.site.register(Goods,GoodsAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderDetail,OrderDetailAdmin)