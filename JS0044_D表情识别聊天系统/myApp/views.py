from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from myApp.models import UserModel
from django.http import JsonResponse
from myApp.chatterbotTest import angry
from myApp.chatterbotTest import disgust
from myApp.chatterbotTest import happy
from myApp.chatterbotTest import neutral
from myApp.chatterbotTest import sad
from myApp.chatterbotTest import scared
from myApp.chatterbotTest import surprised

from myApp.camera import openedCap
import json


class LoginView(View):
    def get(self, request):

        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        userModel = UserModel.objects.filter(email=email).first()
        print("-----1", userModel)
        if userModel is None:
            msg = "该用户不存在"
            print("----")
            return render(request, 'login.html', locals())
        elif userModel.password != password:
            msg = "密码不正确"
            return render(request, 'login.html', locals())

        obj = redirect("/index/")
        obj.set_cookie("is_login", True)
        return obj


#           查询数据库返回
class RegisterView(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        email = request.POST.get("email")
        useranme = request.POST.get("useranme")
        password = request.POST.get("password")
        UserModel.objects.create(email=email, username=useranme, password=password)
        return redirect("/login/")


class IndexView(View):
    def get(self, request):
        is_login = request.COOKIES["is_login"]
        if is_login != "True":
            return redirect("/login")
        return render(request, 'index.html', locals())


class ShowChart(View):
    def get(self, request):
        label = openedCap()
        return render(request, "chartIndex.html", locals())


class ChartView(View):
    def get(self, request):
        chartType = request.GET.get("type")
        return render(request, 'chart.html', locals())


class ChartNow(View):
    def get(self, request):
        charttype = request.GET.get("type")
        content = request.GET.get("content")
        if charttype == "angry":
            aswer = angry.bot(content)
        elif charttype == "disgust":
            aswer = disgust.bot(content)
        elif charttype == "happy":
            aswer = happy.bot(content)
        elif charttype == "neutral":
            aswer = neutral.bot(content)
        elif charttype == "sad":
            aswer = sad.bot(content)
        elif charttype == "scared":
            aswer = scared.bot(content)
        elif charttype == "surprised":
            aswer = surprised.bot(content)
        else:
            aswer = "无法识别"

        return JsonResponse({"content": content, "aswer": aswer})
