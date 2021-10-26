from django.shortcuts import render,redirect

# Create your views here.
from user.models import User
from django.contrib.auth import authenticate, login, logout  # 登入和登出
import uuid
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
        if "." not  in email.split("@")[-1]:
            if password != password2:
                msg = "邮箱不正确"
                return render(request, 'signup.html', locals())

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


def personView(request):
    user=User.objects.filter(id=request.user.id).first()
    return render(request,"person.html",locals())


def changeperson(request):
    if request.method=="POST":
        email=request.POST.get("email")
        username=request.POST.get("username")
        user=User.objects.filter(email=email).first()
        if user is not None:
            msg="该邮箱已经注册"
            return render(request,'edit_person.html',locals())
        user = User.objects.filter(username=username).first()
        if user is not None:
            msg = "该用户名已经注册"
            return render(request, 'edit_person.html', locals())
        user=User.objects.get(id=request.user.id)

        user.email=email
        user.username=username
        user.save()
        return redirect("/person")
    return render(request,'edit_person.html')

def changePic(request):
    if request.method=="POST":
        file=request.FILES.get("file")
        name=file.name
        print(name)
        newname=str(uuid.uuid4())+".jpg"
        with open("./static/image/"+newname,"wb") as f:
            f.write(file.read())
        user=User.objects.get(id=request.user.id)
        user.pic="/image/"+newname
        user.save()

        return redirect("/person/")

    return render(request,'edit_pic.html')