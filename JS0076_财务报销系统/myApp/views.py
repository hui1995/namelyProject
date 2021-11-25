from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.views import View

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
  # 登入和登出






def logoutAdmin(request):
    logout(request)
    return redirect("/login")

@login_required
def homeView(request):
    return render(request, "index.html", locals())





class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', locals())

    def post(self, request):
        username = request.POST.get("username", None)  # 验证码答案
        password = request.POST.get("password", None)  # 验证码答案

        user = authenticate(username=username, password=password)  # 类型为<class 'django.contrib.auth.models.User'>

        if user:
            login(request, user)  # 验证成功之后登录
            return redirect("/")
        else:
            msg = "账号或者密码不正确"
        return render(request, "login.html", locals())

