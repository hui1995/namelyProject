from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.views import View
from myApp.models import User, Dept, CarApply, CarApplyLink, Car,CarLog
import json
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required  # 验证用户是否登录


def logoutAdmin(request):
    logout(request)
    return redirect("/login")


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', locals())

    def post(self, request):
        username = request.POST.get("no", None)  #
        password = request.POST.get("password", None)  # 验证码答案
        user = authenticate(username=username, password=password)  # 类型为<class 'django.contrib.auth.models.User'>

        if user:
            login(request, user)  # 验证成功之后登录
            return redirect("/")
        else:
            msg = "账号或者密码不正确"
        return render(request, "login.html", locals())


def SignUpView(request):
    if request.method == "GET":
        return render(request, 'signup.html', locals())
    elif request.method == "POST":
        no = request.POST.get("no", None)
        phone = request.POST.get("phone", None)
        password = request.POST.get("password", None)
        password2 = request.POST.get("password2", None)
        name = request.POST.get("name", None)
        if password != password2:
            msg = "两次密码不一致"
            return render(request, 'signup.html', locals())
        user = User.objects.filter(username=no).first()
        if user is not None:
            msg = "该警号已经存在"
            return render(request, 'signup.html', locals())

        user = User.objects.create_user(username=no, password=password, email=phone + "@admin")
        user.phone = phone
        user.name = name
        user.save()
        return redirect("/login/")


# 用户列表
@login_required
def deptList(request):
    if request.method == "GET":
        page = request.GET.get("page")
        if page is None or page == "":
            page = 1
        dept = Dept.objects.all().order_by("-id")
        paginator = Paginator(dept, 10)
        page = paginator.page(page)  # 传递当前页的实例对象到前端
        return render(request, 'dept_list.html', locals())


@login_required
def deptDel(request):
    id = request.GET.get("id")
    Dept.objects.filter(id=id).delete()
    return redirect("/dept/list/")


@login_required
def deptOption(request):
    id = request.GET.get("id")
    if id is not None and id != "":
        dept = Dept.objects.filter(id=id).first()
    if request.method == "GET":
        return render(request, 'dept_option.html', locals())

    no = request.POST.get("no")
    name = request.POST.get("name")

    if id is not None and id != "":
        dept.no = no
        dept.name = name
        dept.save()
    else:
        Dept.objects.create(no=no, name=name)
    return redirect("/dept/list/")


def userList(request):
    if request.method == "GET":
        page = request.GET.get("page")
        if page is None or page == "":
            page = 1

        userList = User.objects.all()
        keyword = request.GET.get("keyword", None)
        if keyword is not None and keyword != "":
            userList = userList.filter(name__contains=keyword.strip())
        userList = userList.order_by("-id")
        paginator = Paginator(userList, 10)
        page = paginator.page(page)  # 传递当前页的实例对象到前端

    return render(request, 'user_list.html', locals())


@login_required
def userDel(request):
    id = request.GET.get("id")
    User.objects.filter(id=id).delete()
    return redirect("/user/list/")


# 用户编辑
@login_required
def userEdit(request):
    id = request.GET.get("id")
    user = User.objects.filter(id=id).first()
    deptList = Dept.objects.all()
    if request.method == "GET":
        return render(request, 'userOption.html', locals())
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    deptId = request.POST.get("dept")
    role = request.POST.get("role")
    if deptId is not None and deptId != "":
        dept = Dept.objects.get(id=deptId)
        user.deptId = dept

    user.name = name
    user.phone = phone
    user.role = role
    user.save()
    return redirect("/user/list/")


# 添加申请表单
@login_required
def CarApplyList(request):
    if request.method == "GET":
        page = request.GET.get("page")
        if page is None or page == "":
            page = 1

        carApplyList = CarApply.objects.filter(dept=request.user.deptId)
        keyword = request.GET.get("keyword", None)
        if keyword is not None and keyword != "":
            carApplyList = carApplyList.filter(basis__contains=keyword.strip())
        carApplyList = carApplyList.order_by("-id")
        paginator = Paginator(carApplyList, 10)
        page = paginator.page(page)  # 传递当前页的实例对象到前端

    return render(request, 'car_apply_list.html', locals())


@login_required
def CarApplyDetail(request):
    id = request.GET.get("id")
    carApply = CarApply.objects.filter(id=id).first()
    carApplyLink = CarApplyLink.objects.filter(applyId=carApply).all()
    for i in carApplyLink:
        print(i.remark)
        print(i.status)
    return render(request, 'car_apply_detail.html', locals())


@login_required
def CarApplyApply(request):
    if request.method == "GET":
        return render(request, 'car_apply_option.html', locals())
    basis = request.POST.get("basis")
    place = request.POST.get("place")
    cause = request.POST.get("cause")
    desti = request.POST.get("desti")
    penum = request.POST.get("penum")
    usetime = request.POST.get("usetime")
    gettime = request.POST.get("gettime")
    user = User.objects.get(id=request.user.id)
    carApply = CarApply.objects.create(dept=user.deptId, user=request.user, basis=basis, place=place, cause=cause,
                                       desti=desti,
                                       penum=penum,
                                       usetime=usetime, gettime=gettime, flow_rank=1, status="waiting")

    carApplyLink = CarApplyLink.objects.create(applyId=carApply, status="waiting")
    carApply.flow_id = carApplyLink.id
    carApply.save()

    return redirect("/car/apply/list/")


# 车列表
def carList(request):
    page = request.GET.get("page")
    if page is None or page == "":
        page = 1
    if request.user.deptId.no == "01":
        carList = Car.objects.all()
    else:
        carList = Car.objects.filter(dept=request.user.deptId)
    keyword = request.GET.get("keyword", None)
    if keyword is not None and keyword != "":
        carList = carList.filter(no=keyword)
    carList = carList.order_by("-id")
    paginator = Paginator(carList, 10)
    page = paginator.page(page)  # 传递当前页的实例对象到前端
    return render(request, 'car_list.html', locals())


@login_required
def carDel(request):
    id = request.GET.get("id")
    Car.objects.get(id=id).delete()
    return redirect("/car/list/")


@login_required
def carOption(request):
    id = request.GET.get("id")
    if id is not None and id != "":
        car = Car.objects.filter(id=id).first()
    if request.method == "GET":
        return render(request, 'car_option.html', locals())
    no = request.POST.get("no")
    type = request.POST.get("type")
    nums = request.POST.get("nums")
    knmus = request.POST.get("knmus")
    address = request.POST.get("address")
    status = request.POST.get("status")
    if id is None or id == "":
        dept = Dept.objects.filter(no="01").first()
        Car.objects.create(no=no, type=type, nums=nums, knmus=knmus, address=address, status=status, dept=dept)
    else:
        car.no = no
        car.type = type
        car.nums = nums
        car.knmus = knmus
        car.address = address
        car.status = status
        car.save()
    return redirect("/car/list/")
@login_required
def carAllocation(request):
    id = request.GET.get("id")
    car = Car.objects.filter(id=id).first()
    deptList=Dept.objects.all()
    if request.method == "GET":
        return render(request, 'car_option_allocation.html', locals())

    dept=request.POST.get("dept")
    car.dept_id=dept
    car.save()

    return redirect("/car/list/")

# 用车审核
@login_required
def CarAuthList(request):
    user = request.user
    page = request.GET.get("page")
    print(user.role)
    if page is None or page == "":
        page = 1
    if request.user.role == 1 and request.user.deptId.no != "01":

        carApplyList = CarApply.objects.filter(flow_rank=1).filter(dept=user.deptId)
    elif request.user.deptId is not None and request.user.deptId.no == "01" and request.user.role == 0:
        carApplyList = CarApply.objects.filter(flow_rank=2)
    elif request.user.deptId is not None and request.user.deptId.no == "01" and request.user.role == 1:
        carApplyList = CarApply.objects.filter(flow_rank=3)
    elif request.user.role == 2:
        carApplyList = CarApply.objects.filter(flow_rank=4)
    elif request.user.role == 3:
        print("------")
        carApplyList = CarApply.objects.filter(flow_rank=5)
    else:
        return render(request, 'car_auth_list.html', locals())

    carApplyList = carApplyList.order_by("-id")
    paginator = Paginator(carApplyList, 10)
    page = paginator.page(page)  # 传递当前页的实例对象到前端
    return render(request, 'car_auth_list.html', locals())


import datetime


@login_required
def CarAuthNow(request):
    id = request.GET.get("id")
    if id is not None and id != "":
        carApply = CarApply.objects.filter(id=id).first()
    if request.method == "GET":
        return render(request, 'car_apply_auth.html', locals())
    id = request.GET.get("id")
    status = request.POST.get("status")
    remark = request.POST.get("remark")
    carApply = CarApply.objects.filter(id=id).first()
    carApplyLink = CarApplyLink.objects.filter(id=carApply.flow_id).first()
    carApplyLink.status = status
    carApplyLink.userId = request.user
    carApplyLink.update_time = datetime.datetime.now()
    carApplyLink.remark = remark

    if status == "pass":
        if carApply.flow_rank == 5:
            carApply.status = "pass"
            carApply.flow_rank+=1
            carApply.save()
            carApplyLink.save()
            return redirect("/car/auth/list/")
        else:
            carApply.status = "reviewing"
        flow_rank = carApply.flow_rank
        flow_rank += 1

        carApply.flow_rank = flow_rank
    else:
        carApply.status = "fail"
    carApplyLink.save()
    carApplyLink = CarApplyLink.objects.create(applyId=carApply, status="waiting")
    carApply.flow_id = carApplyLink.id

    carApply.save()
    carApplyLink.save()
    return redirect("/car/auth/list/")


@login_required
def index(request):
    if request.user.role in(1,2,3):
        return redirect("/car/auth/list/")
    return redirect("/car/list/")


# 车列表
@login_required
def carOptionList(request):
    id=request.GET.get("id")
    page = request.GET.get("page")
    carLog=CarLog.objects.filter(car_id=id)
    if page is None or page == "":
        page = 1
    keyword = request.GET.get("keyword", None)

    carLog = carLog.order_by("-id")
    paginator = Paginator(carLog, 10)
    page = paginator.page(page)  # 传递当前页的实例对象到前端
    return render(request, 'car_option_list.html', locals())

@login_required
def carOptionAdd(request):
    if request.method=="GET":
        return render(request,'car_option_add.html')
    id=request.GET.get("id")
    type=request.POST.get("type")
    remark=request.POST.get("remark")
    date=request.POST.get("date")
    CarLog.objects.create(user=request.user,remark=remark,option_type=type,create_time=date)

    return redirect("/car/option/list/?id="+id)
