from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.views import View
import json
from django.contrib.auth import authenticate, login, logout  # 登入和登出
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from myApp.models import User,Theme,Course,CourseDetail,GroupModel,CourseStudent,GroupStudent







def logoutAdmin(request):
    logout(request)
    return redirect("/login")
@login_required
def indexVIew(request):
    if request.user.type==0:
        return redirect("/stu/course/list/")
    else:
        return redirect("/course/list/")


class TeaIndexView(View):
    def get(self, request):
        return render(request, 'index.html', locals())
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', locals())

    def post(self, request):
        username = request.POST.get("username", None)  # 验证码答案
        password = request.POST.get("password", None)  # 验证码答案
        user = authenticate(username=username, password=password)  # 类型为<class 'django.contrib.auth.models.User'>
        if user:
            login(request, user)  # 验

            return redirect("/")
     
        else:
            msg = "账号或者密码不正确"
        return render(request, "login.html", locals())

class TeaSignUpView(View):
    def get(self, request):
        return render(request, 'teasignup.html', locals())

    def post(self, request):
        username = request.POST.get("username", None)  
        password = request.POST.get("password", None)  
        birtday = request.POST.get("birtday", None) 
        sex = request.POST.get("sex", None) 
        summary = request.POST.get("summary", None) 
        password2 = request.POST.get("password2", None)  
        email = request.POST.get("email", None)  
        if password!=password2:
            msg = "两次密码不一致"
            return render(request, "teasignup.html", locals())
        User.objects.create_user(username=username, password=password, email=email,birtday=birtday,sex=sex,summary=summary,type=1)        
        return redirect("/login/")

class StuSignUpView(View):
    def get(self, request):
        return render(request, 'stusignup.html', locals())

    def post(self, request):
        username = request.POST.get("username", None)  
        password = request.POST.get("password", None)  
        birtday = request.POST.get("birtday", None) 
        sex = request.POST.get("sex", None) 
        summary = request.POST.get("summary", None) 
        password2 = request.POST.get("password2", None)  
        email = request.POST.get("email", None)  
        grade = request.POST.get("grade", None)  
        if password!=password2:
            msg = "两次密码不一致"
            return render(request, "stusignup.html", locals())
        User.objects.create_user(username=username, password=password, email=email,birtday=birtday,sex=sex,summary=summary,type=0,grade=grade)        
        return redirect("/login/")

@login_required
def themeList(request):
    keyword = request.GET.get("keyword", None)  
    result=Theme.objects.filter(user=request.user)
    if keyword is not None:
        result=result.filter(name__contains=keyword)
    return render(request,"themelist.html",locals())
@login_required
def themeAdd(request):
    if request.method=="GET":
        return render(request,"themeAdd.html")
    name = request.POST.get("name", None)  
    Theme.objects.create(name=name,user=request.user)
    return redirect("/theme/list/")
@login_required
def themeEdit(request):
    id = request.GET.get("id", None)  
    theme=Theme.objects.get(id=id)
    if request.method=="GET":   
        return render(request,"themeEdit.html",locals())
    name = request.POST.get("name", None)  
    theme.name=name
    theme.save()
    return redirect("/theme/list/")
@login_required
def themeDel(request):
    id = request.GET.get("id", None)  
    theme=Theme.objects.get(id=id).delete()
    return redirect("/theme/list/")

@login_required
def CourseList(request):
    result=CourseDetail.objects.filter(user=request.user)
    return render(request,"courselist.html",locals())
@login_required
def CourseDetailView(request):
    id=request.GET.get("id")
    grouplist=GroupModel.objects.filter(course__id=id)
    userlist=CourseStudent.objects.filter(course__id=id)
    
    return render(request,"courseDetail.html",locals())

#创建小组
@login_required
def GroupAddView(request):
    courseid=request.GET.get("courseid")
    if request.method=="GET":
        themelist=Theme.objects.filter(user=request.user)
        return render(request,"groupAdd.html",locals())
    number=request.POST.get("number")
    theme=request.POST.get("theme")
    GroupModel.objects.create(number=number,theme_id=theme,course_id=courseid)
    return redirect("/course/detail/?id="+courseid)
#删除小组
@login_required
def GroupDelView(request):
    id=request.GET.get("id")
    courseid=request.GET.get("courseid")
    GroupModel.objects.get(id=id).delete()
    GroupStudent.objects.filter(groupModel__id=id).delete()
    return redirect("/course/detail/?id="+courseid)

#查询小组成员
@login_required
def GroupStuListView(request):
    id=request.GET.get("id")
    courseid=request.GET.get("courseid")
    groupStudentList= GroupStudent.objects.filter(groupModel__id=id)
    return render(request,"groupDetailList.html",locals())

#添加成员
@login_required
def GroupStuAddView(request):

    courseid=request.GET.get("courseid")
    groupid=request.GET.get("groupid")
    if request.method=="GET":
        courseStuList=CourseStudent.objects.filter(course__id=courseid)
        grouplistStuList=GroupStudent.objects.filter(groupModel__course__id=courseid)
        lst=[]
        for i in grouplistStuList:
            lst.append(i.user.id)
        result=[]
        for i in courseStuList:
            if i.user.id not in lst:
                dict1={}
                dict1["id"]=i.user.id
                dict1["username"]=i.user.username
                result.append(dict1)      
        return render(request,"groupStuAdd.html",locals())
    id=request.POST.get("id")
    GroupStudent.objects.create(groupModel_id=groupid,user_id=id)
    # GroupStudent
    return redirect("/group/stu/list/?id="+groupid+"&courseid="+courseid)

#移除成员
@login_required
def GroupStuDelView(request):
    id=request.GET.get("id")
    courseid=request.GET.get("courseid")
    groupid=request.GET.get("groupid")
    GroupStudent.objects.get(id=id).delete()
    return redirect("/group/stu/list/?id="+groupid+"&courseid="+courseid)

@login_required
def GroupStuLeaderView(request):
    id=request.GET.get("id")
    courseid=request.GET.get("courseid")
    groupid=request.GET.get("groupid")
    groupStudent=GroupStudent.objects.get(id=id)
    leaderINfo=GroupStudent.objects.filter(groupModel__id=groupid)
    if leaderINfo is not None:
        leaderINfo=leaderINfo.filter(type=1).first()
        if leaderINfo is not None:
            leaderINfo.type=0
            leaderINfo.save()
    groupStudent.type=1
    groupStudent.save()
    return redirect("/group/stu/list/?id="+groupid+"&courseid="+courseid)

@login_required
def StuCourseListView(request):
    courselist=Course.objects.all()
    courseStuList=CourseStudent.objects.filter(user=request.user)
    lst=[]
    for i in courseStuList:
        lst.append(i.course.course.id)
    result=[]
    for i in courselist:
        dict1={}
        dict1["title"]=i.title
        dict1["credit"]=i.credit
        dict1["score"]=i.score
        dict1["id"]=i.id
        if i.id in lst:
            dict1["selected"]=True
        else:
            dict1["selected"]=False
        result.append(dict1)
    return render(request,"stucourselist.html",locals())


@login_required
def StuCourseDetailListView(request):
    id=request.GET.get("id")
    result=CourseDetail.objects.filter(course__id=id)
    return render(request,"courselistselected.html",locals())
@login_required
def selectedCourseNow(request):
    id=request.GET.get("id")
    CourseStudent.objects.create(course_id=id,user=request.user)
    return redirect("/stu/course/list/")




#我的选课
@login_required
def MyStuCourseListView(request):
    result=CourseStudent.objects.filter(user=request.user)
    return render(request,"mycourselist.html",locals()) 

# 我的分组
@login_required
def MyStuGroupListView(request):
    result=GroupStudent.objects.filter(user=request.user)
    return render(request,"mygrouplist.html",locals())     
