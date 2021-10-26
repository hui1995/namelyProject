from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.template import loader
from django.views import View
import json
from feature_select import main_indian_pines
from django.contrib.auth import authenticate, login, logout  # 登入和登出
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required  # 验证用户是否登录
from myApp.models import User
from QEA import main
from FeatureSelectionGA import abalone_test,cmc_test,colon_test,glass_test,iris_test,sonar_test,wine_test,lung_small_test
import numpy as np
def logoutAdmin(request):
    logout(request)
    return redirect("/login")


def change_admin_password(request):
    if request.method == "GET":
        return render(request, 'change_passwod.html')
    password1 = request.POST.get("password")
    password2 = request.POST.get("password2")
    if password1 != password2:
        msg = "两次密码不一致"
        return render(request, 'change_passwod.html', locals())
    admin = User.objects.get(id=request.user.id)
    admin.set_password(password1)
    admin.save()

    return redirect("/login")




class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', locals())

    def post(self, request):
        username = request.POST.get("no", None)  #
        password = request.POST.get("password", None)  # 验证码答案
        user = authenticate(username=username, password=password)  # 类型为<class 'django.contrib.auth.models.User'>

        if user:
            return redirect("/index")
        else:
            msg = "账号或者密码不正确"
        return render(request, "login.html", locals())


def SignUpView(request):
    if request.method == "GET":
        return render(request, 'signup.html', locals())
    elif request.method == "POST":
        username = request.POST.get("no", None)
        password = request.POST.get("password", None)
        password2 = request.POST.get("password2", None)
        name = request.POST.get("name", None)
        if password != password2:
            msg = "两次密码不一致"
            return render(request, 'signup.html', locals())
        user = User.objects.filter(username=username).first()
        if user is not None:
            msg = "该用户已经存在"
            return render(request, 'signup.html', locals())

        user = User.objects.create_user(username=username, password=password, email=username + "@admin")
        return redirect("/login/")

@login_required
def IndexView(request):
    return render(request,'index.html',locals())
@login_required
def CommentView(request):
    return render(request,'comment.html',locals())

@login_required
def FaView(request):
    if request.method=="GET":
        return render(request,'fa.html',locals())
    data=request.FILES.get("data")
    filename=data.name

    if "abalone" in filename:
        score=abalone_test.main(data)
    elif "cmc" in filename:
        score = cmc_test.main(data)

    elif "colon" in filename:
        score=colon_test.main(data)
    elif "glass" in filename:
        score=glass_test.main(data)
    elif "iris" in filename:
        score=iris_test.main(data)
    elif "lung_small" in filename:
        score=lung_small_test.main(data)
    elif "sonar" in filename:
        score=sonar_test.main(data)
    elif "wine" in filename:
        score=wine_test.main(data)
    else:
        score="该数据集不正确"



    # print(data)
    return render(request,'fa.html',locals())
@login_required
def acoView(request):
    if request.method=="GET":
        return render(request,'aco.html',locals())
#     main_indian_pines
    input_info=request.FILES.get("input_info")
    output_info=request.FILES.get("output_info")
    result=main_indian_pines.main(input_info,output_info)
    return render(request, 'aco.html', locals())
@login_required
def qeaView(request):
    if request.method=="GET":
        return render(request,'qea.html',locals())

    data=request.FILES.get("data")
    info=data.read().decode("utf-8").split("\n")
    result=main.main(info)
    return render(request,'qea.html',locals())





def uploadDate(request):
    data=request.FILES.get("data")
    data=data.read().decode("utf-8")
    data=data.split("\n")
    result=[]
    for i in data:
        info=i.split(",")
        result.append(info)

    return JsonResponse({"data":result})

