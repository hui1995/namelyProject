from django.shortcuts import render,redirect
from django.views import View
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout

from myApp.models import CommentsModel, User

from datetime import datetime


# Create your views here.

class HomeView(View):
    def get(self,request):
        return render(request,'home.html')

    def post(self,request):
        
        return redirect("")
class InformationView(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        return render(request,'information.html')
class MemebersView(View):
    def get(self,request):
        if  not request.user.is_authenticated:
            return render(request, 'login.html')        
        return render(request,'memeber.html')


class LoginView(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        username=request.POST.get("username")
        password=request.POST.get("password")
        if username is None or password is None:
            message="用户吗和密码不能为空"
            return render(request,"login.html",locals())
        user = authenticate(request, username=username, password=password)      
        # 验证如果用户不为空
        if user is not None:
            # login方法登录
            login(request, user)
            # 返回登录成功信息
            return redirect("/")
        else:
            # 返回登录失败信息
            message="用户名或者密码错误"
            return render(request,"login.html",locals())


class MessageView(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return render(request, 'login.html')    
        commentList=CommentsModel.objects.all().order_by("-id")    
        return render(request,'message.html',locals())

    def post(self,request):
        content=request.POST.get("content")
        CommentsModel.objects.create(content=content,createDate=datetime.now(),user=request.user)
        return redirect("/message")
class DelMessageView(View):
    def get(self,request):
        id=request.GET.get("id")
        CommentsModel.objects.filter(id=id).delete()
        return redirect("/message")


class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("/login/")