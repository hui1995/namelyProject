from django.shortcuts import render, redirect
from django.http import JsonResponse
from goods.models import Goods, CollectGoods, Cart, Order, OrderDetail, Address,Message
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required

def index(request):
    goodslist = Goods.objects.all().order_by("-sold")
    if len(goodslist) > 3:
        goodslist = goodslist[0:3]
    return render(request, 'index.html', locals())


def hotGoodList(request):
    cate = request.GET.get("cate")
    page = request.GET.get("page")
    if page is None or page == "":
        page = 1
    if cate == "hot":
        title = "热卖商品"
        goodslist = Goods.objects.all().order_by("-sold")
    else:
        title = "最新上架"
        goodslist = Goods.objects.all().order_by("-publish_date","-id")
    paginator = Paginator(goodslist, 18)
    page1 = paginator.page(page)  # 第1页的page对象

    return render(request, 'goodList.html', locals())


def searchGoodList(request):
    keyword = request.GET.get("keyword")
    page = request.GET.get("page")
    if page is None or page == "":
        page = 1
    if keyword is not None:
        keyword=keyword.strip()
    title = keyword

    goodslist = Goods.objects.filter(name__contains=keyword)
    paginator = Paginator(goodslist, 18)
    page1 = paginator.page(page)  # 第1页的page对象

    return render(request, 'goodList.html', locals())


def goodsDetail(request):
    id = request.GET.get("id")
    if request.method=="POST":
        message=request.POST.get("message")
        Message.objects.create(goods_id=id,user_id=request.user.id,message=message)
        return redirect("/goods/detail/?id="+id)
    goods = Goods.objects.get(id=id)
    collectGoods = CollectGoods.objects.filter(goods_id=id).filter(user_id=request.user.id).first()
    if collectGoods is None:
        collect = False
    else:
        collect = True
    messageList=Message.objects.filter(goods_id=id)

    return render(request, 'goodsDetail.html', locals())

@login_required
def collectGoods(request):
    id = request.GET.get("id")
    goods = Goods.objects.get(id=id)
    collectGoods = CollectGoods.objects.filter(goods_id=id).filter(user_id=request.user.id).first()
    if collectGoods is None:
        CollectGoods.objects.create(goods_id=id, user_id=request.user.id)
        goods.collect += 1
    else:
        collectGoods.delete()
        goods.collect -= 1
    goods.save()
    return redirect("/goods/detail/?id=" + id)


# 获取购物车信息
@login_required
def cartList(request):
    if request.method == "GET":
        cartList = Cart.objects.filter(user_id=request.user.id)
        if len(cartList)==0:
            cart=None
        return render(request, 'cart.html', locals())


# 订单下单按钮
@login_required
def orderNow(request):
    id = request.GET.get("id")
    num = request.GET.get("num")
    if id=="cart":
        goods=Goods.objects.filter(cart__user_id=request.user.id)
        cart = Cart.objects.filter(user_id=request.user.id)
        for i in cart:
            if i.goods.stock<i.num:
                msg = "订单数量超出库存数量"
                return render(request, "order.html", locals())

    else:

        goods = Goods.objects.filter(id=id)
        for i in goods:
            if i.stock < int(num):
                msg = "订单数量超出库存数量"
                return render(request, "order.html", locals())

    addressList = Address.objects.filter(user_id=request.user.id)

    if request.method == "POST":
        address = request.POST.get("address")
        order = Order.objects.create(status=0, user_id=request.user.id, address_id=address)
        total_price = 0.0
        for i in goods:
            if id=="cart":
                cart=Cart.objects.filter(goods_id=i.id).filter(user_id=request.user.id).first()
                if cart is None:
                    continue
                OrderDetail.objects.create(order_id=order.id, goods_id=i.id, price=i.price,num=cart.num)
                cart.delete()
                total_price += float(i.price)
                i.stock -= cart.num
                i.sold += cart.num
                i.save()
            else:
                OrderDetail.objects.create(order_id=order.id, goods_id=i.id, price=i.price, num=num)
                total_price += float(i.price)

                i.stock -=int(num)
                i.sold += int(num)
                i.save()
        order.total_price = total_price
        order.save()
        return redirect("/order/succeed/")

    return render(request, 'order.html', locals())

@login_required
def ordersucceed(request):
    return render(request, 'orderSucceed.html', locals())

@login_required
def addresslist(request):
    id = request.GET.get("id")

    if request.method == "POST":
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        if username is None or username=="":
            msg="姓名不能为空"
            return render(request, 'address.html', locals())
        if phone is None or phone == "":
            msg = "手机号不能为空"
            return render(request, 'address.html', locals())
        if address is None or address == "":
            msg = "地址不能为空"
            return render(request, 'address.html', locals())

        Address.objects.create(username=username, phone=phone, address=address, user_id=request.user.id)
        return redirect("/goods/order/?id=" + id)
    return render(request, 'address.html', locals())

@login_required
def orderList(request):
    order=Order.objects.filter(user_id=request.user.id).order_by("-id")
    return render(request, 'orderList.html',locals())
@login_required
def orderDetailList(request):
    id=request.GET.get("id")
    orderDetailList=OrderDetail.objects.filter(order_id=id)
    return render(request,'orderDetailList.html',locals())
@login_required
def orderStatus(request):
    id=request.GET.get("id")
    order=Order.objects.filter(id=id).first()
    order.status=2
    order.save()
    return redirect("/order/list/")
 #购物车列表
@login_required
def cartList(request):
    cartList=Cart.objects.filter(user_id=request.user.id)
    total_price=0
    for i in cartList:
        total_price+=(float(i.goods.price)*i.num)
    if len(cartList)==0:
        cart=False
    else:
        cart=True
    return render(request,'cart.html',locals())

 #添加购物车
def cartAdd(request):
    id=request.GET.get("id")
    num=request.GET.get("num")
    cart=Cart.objects.filter(goods_id=id).first(user_id=request.user.id).first()
    if cart is None:
        Cart.objects.create(goods_id=id,user_id=request.user.id,num=num)
    else:
        cart.num+=int(num)
        cart.save()
    return JsonResponse({"code":1,"msg":"添加购物车成功"})


def cartDel(request):
    id=request.GET.get("id")
    Cart.objects.get(id=id).delete()
    return redirect("/cart/list/")

def delorder(request):
    id=request.GET.get("id")
    order=Order.objects.get(id=id)
    order.status=3
    order.save()
    return redirect("/order/list/")

def Home(request):
    return redirect("/index/")

def collectList(request):
    collectGoods=CollectGoods.objects.filter(user_id=request.user.id).order_by("-id")
    return render(request,'collectGoods.html',locals())








