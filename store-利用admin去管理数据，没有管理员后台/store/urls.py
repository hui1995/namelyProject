"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from goods import views as goods
from user import views as user
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', goods.index),
    path('goods/list/', goods.hotGoodList),
    path('goods/search/', goods.searchGoodList),
    path('goods/detail/', goods.goodsDetail),
    path('goods/collect/', goods.collectGoods),
    path('collect/list/', goods.collectList),
    path('goods/order/', goods.orderNow),
    path('goods/address/', goods.addresslist),
    path('order/succeed/', goods.ordersucceed),
    path('login/', user.loginUser),
    path('signup/', user.signup),
    path('logout/', user.logoutuser),
    path('password/', user.changepassword),
    path("order/list/",goods.orderList),
    path("order/status/",goods.orderStatus),
    path("order/del/",goods.delorder),
    path("order/detail/list/",goods.orderDetailList),
    path("cart/add/",goods.cartAdd),
    path("cart/list/",goods.cartList),
    path("cart/del/",goods.cartDel),
    path("",goods.Home)
]
