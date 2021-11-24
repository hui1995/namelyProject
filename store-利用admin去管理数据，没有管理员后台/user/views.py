from django.shortcuts import render,redirect

# Create your views here.
from user.models import User
from django.contrib.auth import authenticate, login, logout  # 登入和登出

def loginUser(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = authenticate(username=username, password=password)  # 类型为<class 'django.contrib.auth.models.User'>

        if user:
            login(request, user)  # 验证成功之后登录
            return redirect("/index/")
        else:
            msg = "账号或者密码不正确"
    return render(request,'login.html',locals())

# signup
def signup(request):
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if len(username)<=3:
            msg="用户名不能低于3位"
            return render(request, 'signup.html', locals())
        if len(password)<=3:
            msg="密码位数过短"
            return render(request, 'signup.html', locals())
        if password!=password2:
            msg="两次密码不一致"
            return render(request, 'signup.html', locals())
        email = request.POST.get("email")
        try:
            user=User.objects.create_user(username,email,password)
            return redirect("/login/")
        except Exception as e:
            print(e)
            msg="用户名或者密码不能重复"
    return render(request,'signup.html',locals())

def logoutuser(request):
    logout(request)
    return redirect("/index/")

def changepassword(request):
    if request.method=="POST":
        password=request.POST.get("password")
        user=User.objects.get(id=request.user.id)
        user.set_password(password)
        user.save()
        logout(request)
        return redirect("/login")
    return render(request,'password.html')
