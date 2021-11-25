from django.shortcuts import render,HttpResponse
from django.template import loader
from django.views import View
import csv
from .models import GameModel,EventModel,Medals
# Create your views here.
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
class LoginView(View):
    def get(self,request):
   

        return render(request,'login.html',locals())

def index(request):

        return render(request,"menu.html",locals())

def search(request):
 
    keyword=request.GET.get("keyword","").strip()
   
    page = request.GET.get('page')  # 获取页码
 
    if keyword is not None and keyword!="":
        result=Medals.objects.filter(Q(city__contains=keyword)|Q(athlete__contains=keyword)|Q(gender__contains=keyword)|Q(country_code__contains=keyword)|Q(medal__contains=keyword)|Q(country__contains=keyword)|Q(gid__sport__contains=keyword)|Q(gid__discipline__contains=keyword)|Q(eid__event__contains=keyword))
        paginator = Paginator(result, 50)  # 实例化一个分页对象

        try:
            result = paginator.page(page)  # 获取某页对应的记录
        except PageNotAnInteger:  # 如果页码不是个整数
            result = paginator.page(1)  # 取第一页的记录
        except EmptyPage:  # 如果页码太大，没有相应的记录
            result = paginator.page(paginator.num_pages)  # 取最后一页的记录

    return render(request,"search.html",locals())

def search2(request):
 
    city=request.GET.get("city","").strip()
    athlete=request.GET.get("athlete","").strip()
    gender=request.GET.get("gender","").strip()
    country_code=request.GET.get("country_code","").strip()
    medal=request.GET.get("medal","").strip()
    country=request.GET.get("country","").strip()
    sport=request.GET.get("sport","").strip()
    discipline=request.GET.get("discipline","").strip()
    event=request.GET.get("event","").strip()
    year=request.GET.get("year","").strip()
    search=request.GET.get("search","").strip()   
    if search is  None or search =="":
        return render(request,"search2.html",locals())
    page = request.GET.get('page')  # 获取页码
    result=Medals.objects.all()

    if city is not None and city!="":
        result=result.filter(city=city)

    if gender is not None and gender!="":
        result=result.filter(gender=gender)
    if athlete is not None and athlete!="":
        result=result.filter(athlete=athlete)
    if country_code is not None and country_code!="":
        result=result.filter(country_code=country_code)
    if medal is not None and medal!="":
        result=result.filter(medal=medal)   
    if country is not None and country!="":
        result=result.filter(country=country)    
    if sport is not None and sport!="":
        result=result.filter(gid__sport=sport)    
    if discipline is not None and discipline!="":
        result=result.filter(gid__discipline=discipline)  
    if event is not None and event!="":
        result=result.filter(event=event)    
    if year is not None and year!="":
        result=result.filter(year=year)          
    paginator = Paginator(result, 50)  # 实例化一个分页对象
    try:
        result = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        result = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        result = paginator.page(paginator.num_pages)  # 取最后一页的记录

    return render(request,"search2.html",locals())