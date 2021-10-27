from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.views import View
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from myApp.models import Admin, AuthRelationAdmin, Auth, Homeowner, Staff, Repair, Report, Complaints, Public, Guest
import json
from django.contrib.auth import authenticate, login, logout  # 登入和登出
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required  # 验证用户是否登录


# 验证码相关
def captcha():
    hashkey = CaptchaStore.generate_key()  # 验证码答案
    image_url = captcha_image_url(hashkey)  # 验证码地址
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    return captcha


# 刷新验证码
def refresh_captcha(request):
    return HttpResponse(json.dumps(captcha()), content_type='application/json')


def logoutAdmin(request):
    logout(request)
    return redirect("/login")


def homeView(request):
    if request.user.is_authenticated:
        return redirect("/admin/index/")
    else:
        return redirect("/index/")

def index(request):
    if request.user.a_auth == 3 or request.user.a_auth == 2:
        return redirect("/admin/list")
    else:
        authList = AuthRelationAdmin.objects.filter(admin_id=request.user.id)
        haveAuthList = []
        for i in authList:
            haveAuthList.append(i.auth_id)
        if 1 in haveAuthList:
            return redirect("/user/list")
        elif 2 in haveAuthList:
            return redirect("/public/list")
        elif 3 in haveAuthList:
            return redirect("/staff/list")
        else:
            return HttpResponse("没有权限访问")


class LoginView(View):
    def get(self, request):
        hashkey = CaptchaStore.generate_key()  # 验证码答案
        image_url = captcha_image_url(hashkey)  # 验证码地址
        captcha = {'hashkey': hashkey, 'image_url': image_url}
        return render(request, 'login.html', locals())

    def post(self, request):
        capt = request.POST.get("code", None)  # 用户提交的验证码
        key = request.POST.get("hashkey", None)  # 验证码答案
        username = request.POST.get("username", None)  # 验证码答案
        password = request.POST.get("password", None)  # 验证码答案
        hashkey = CaptchaStore.generate_key()  # 验证码答案
        image_url = captcha_image_url(hashkey)  # 验证码地址
        captcha = {'hashkey': hashkey, 'image_url': image_url}

        if self.jarge_captcha(capt, key) == False:
            msg = "验证码输入错误"
            return render(request, 'login.html', locals())
        user = authenticate(username=username, password=password)  # 类型为<class 'django.contrib.auth.models.User'>

        if user:
            if user.a_status == 0:
                msg = "账号被冻结"
                return render(request, 'login.html', locals())
            login(request, user)  # 验证成功之后登录

            return redirect("/admin/index/")
        else:
            msg = "账号或者密码不正确"
        return render(request, "login.html", locals())

    def jarge_captcha(self, captchaStr, captchaHashkey):
        if captchaStr and captchaHashkey:
            try:
                # 获取根据hashkey获取数据库中的response值
                get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
                if get_captcha.response == captchaStr.lower():  # 如果验证码匹配
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False


@login_required
def adminEdit(request):
    id = request.GET.get("id", None)
    authList = []
    authHaveList = []

    auth = Auth.objects.all()

    aduthRelationAdmin = AuthRelationAdmin.objects.filter(admin_id=id)
    for i in aduthRelationAdmin:
        authHaveList.append(i.auth_id)
    for i in auth:
        dict1 = {"name": i.name, "id": i.id}
        if i.id not in authHaveList:
            dict1["have"] = False
        else:
            dict1['have'] = True
        authList.append(dict1)
    admin = Admin.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'adminEdit.html', locals())

    username = request.POST.get("username", None)
    phone = request.POST.get("phone", None)
    email = request.POST.get("email", None)
    authId = request.POST.getlist("auth", None)
    adminForUsername = Admin.objects.filter(username=username).first()
    if adminForUsername is not None and adminForUsername.id != int(id):
        msg = "该用户已存在"
        return render(request, 'adminEdit.html', locals())
    adminFOrEmail = Admin.objects.filter(email=email).first()

    if adminFOrEmail is not None and adminFOrEmail.id != int(id):
        msg = "该邮箱已存在"
        return render(request, 'adminEdit.html', locals())
    admin.username = username
    admin.email = email
    admin.a_phone = phone
    admin.save()
    if admin.a_status == 0:
        AuthRelationAdmin.objects.filter(admin_id=id).delete()
        for i in authId:
            request.user.auth = i
            print(request.user.auth)
            AuthRelationAdmin.objects.create(admin_id=admin.id, auth_id=i)
    return redirect("/admin/list")


@login_required
def adminAdd(request):
    if request.method == "GET":
        authList = Auth.objects.all()

        return render(request, 'adminAdd.html', locals())
    elif request.method == "POST":
        username = request.POST.get("username", None)
        phone = request.POST.get("phone", None)
        email = request.POST.get("email", None)
        authId = request.POST.getlist("auth", None)

        admin = Admin.objects.filter(username=username).first()
        admin = Admin.objects.create_user(username=username, password="123456", email=email)
        admin.a_phone = phone
        admin.a_spare = "123456"
        admin.save()
        for i in authId:
            AuthRelationAdmin.objects.create(admin_id=admin.id, auth_id=i)
        return redirect("/admin/list/")


@login_required
def adminDel(request):
    id = request.GET.get("id")
    Admin.objects.filter(id=id).delete()
    authRelationAdmin = AuthRelationAdmin.objects.filter(admin_id=id).all()
    for i in authRelationAdmin:
        i.delete()
    return redirect("/admin/list")


@login_required
def adminList(request):
    if request.method == "GET":
        page = request.GET.get("page")
        if page is None or page == "":
            page = 1

        adminList = Admin.objects.filter(a_auth=1)
        keyword = request.GET.get("keyword", None)
        if keyword is not None and keyword!="":
            adminList=adminList.filter(username__contains=keyword)
        adminList=adminList.order_by("-id")
        paginator = Paginator(adminList, 7)
        page = paginator.page(page)  # 传递当前页的实例对象到前端
        datalist = []
        for i in page.object_list:
            data = {}

            data["admin"] = i
            authRelationAdmin = AuthRelationAdmin.objects.filter(admin_id=i.id)
            authDict = ""
            for i in authRelationAdmin:
                auth = Auth.objects.get(id=i.auth_id)
                authDict+=auth.name
                authDict+=","
            data['auth'] = authDict[:-1]
            datalist.append(data)
    return render(request, 'admin_list.html', locals())


@login_required
def adminStatusList(request):
    if request.method == "GET":
        page = request.GET.get("page")
        if page is None or page == "":
            page = 1
        adminList = Admin.objects.filter(a_auth=1)
        keyword = request.GET.get("keyword", None)
        if keyword is not None and keyword != "":
            adminList = adminList.filter(username__contains=keyword)
        adminList=adminList.order_by("-id")
        paginator = Paginator(adminList, 7)
        page = paginator.page(page)  # 传递当前页的实例对象到前端
        datalist = []
        for i in page.object_list:
            data = {}

            data["admin"] = i
            authRelationAdmin = AuthRelationAdmin.objects.filter(admin_id=i.id)
            authDict = ""
            for i in authRelationAdmin:
                auth = Auth.objects.get(id=i.auth_id)
                authDict += auth.name
                authDict += ","
            data['auth'] = authDict[:-1]
            datalist.append(data)
    return render(request, 'admin_status_list.html', locals())


def adminChangeStatus(request):
    id = request.GET.get("id")
    type = request.GET.get("type")
    admin = Admin.objects.get(id=id)
    admin.a_status = type
    admin.save()
    return redirect("/admin/status/list/")


@login_required
def UserOption(request):
    id = request.GET.get("id")
    homeowner = Homeowner.objects.filter(id=id).first()
    if request.method == "GET":
        return render(request, 'userOption.html', locals())
    elif request.method == "POST":
        h_house = request.POST.get("h_house", None)
        h_name = request.POST.get("h_name", None)
        h_id = request.POST.get("h_id", None)
        h_phone = request.POST.get("h_phone", None)
        h_cname = request.POST.get("h_cname", None)
        h_cphone = request.POST.get("h_cphone", None)
        if id is None or id == "":
            Homeowner.objects.create(h_cname=h_cname, h_cphone=h_cphone, h_name=h_name, h_id=h_id, h_house=h_house,
                                     h_phone=h_phone, h_password="123456", h_sparce="123456")
        else:
            homeowner.h_cphone = h_cphone
            homeowner.h_house = h_house
            homeowner.h_name = h_name
            homeowner.h_phone = h_phone
            homeowner.h_cname = h_cname
            homeowner.save()

        return redirect("/user/list/")


@login_required
def userDel(request):
    id = request.GET.get("id")
    Homeowner.objects.filter(id=id).delete()
    return redirect("/user/list")


@login_required
def userList(request):
    if request.method == "GET":
        if request.user.a_auth == 1:
            auth = AuthRelationAdmin.objects.filter(admin_id=request.user.id).filter(auth_id=1).first()
            if auth is None:
                return render(request, 'user_list.html', locals())
        auth = True

        page = request.GET.get("page")
        if page is None or page == "":
            page = 1
        keyword = request.GET.get("keyword", None)
        if keyword is not None and keyword != "":
            homeowner = Homeowner.objects.filter(h_name__contains=keyword).order_by("-id")
        else:
            homeowner = Homeowner.objects.order_by("-id")

        paginator = Paginator(homeowner, 7)
        page = paginator.page(page)  # 传递当前页的实例对象到前端
    return render(request, 'user_list.html', locals())


#

# 职工管理

@login_required
def StaffOption(request):
    id = request.GET.get("id")
    staff = Staff.objects.filter(id=id).first()
    if request.method == "GET":
        return render(request, 'staffOption.html', locals())
    elif request.method == "POST":
        s_number = request.POST.get("s_number", None)
        s_name = request.POST.get("s_name", None)
        d_name = request.POST.get("d_name", None)
        j_name = request.POST.get("j_name", None)
        s_explan = request.POST.get("s_explan", None)
        s_id = request.POST.get("s_id", None)
        s_phone = request.POST.get("s_phone", None)
        s_cname = request.POST.get("s_cname", None)
        s_cphone = request.POST.get("s_cphone", None)
        if id is None or id == "":
            Staff.objects.create(s_number=s_number, s_name=s_name, d_name=d_name, j_name=j_name, s_explan=s_explan,
                                 s_id=s_id, s_phone=s_phone, s_cname=s_cname, s_cphone=s_cphone)
        else:
            staff.s_number = s_number
            staff.s_name = s_name
            staff.d_name = d_name
            staff.j_name = j_name
            staff.s_explan = s_explan
            staff.s_id = s_id
            staff.s_phone = s_phone
            staff.s_cname = s_cname
            staff.s_cphone = s_cphone
            staff.save()

        return redirect("/staff/list/")


@login_required
def staffDel(request):
    id = request.GET.get("id")
    Staff.objects.filter(id=id).delete()
    return redirect("/staff/list")


@login_required
def staffList(request):
    if request.method == "GET":

        if request.user.a_auth == 1:
            auth = AuthRelationAdmin.objects.filter(admin_id=request.user.id).filter(auth_id=3).first()
            if auth is None:
                return render(request, 'user_list.html', locals())
        auth = True
        page = request.GET.get("page")
        if page is None or page == "":
            page = 1

        keyword = request.GET.get("keyword", None)
        if keyword is not None and keyword != "":
            staffList = Staff.objects.filter(s_name__contains=keyword).order_by("-id")
        else:
            staffList = Staff.objects.order_by("-id")
        paginator = Paginator(staffList, 7)
        page = paginator.page(page)  # 传递当前页的实例对象到前端
    return render(request, 'staff_list.html', locals())


# public

# 宣传管理
@login_required
def PublicOption(request):
    id = request.GET.get("id")
    public = Public.objects.filter(id=id).first()
    if request.method == "GET":
        return render(request, 'publicOption.html', locals())
    elif request.method == "POST":
        p_title = request.POST.get("p_title", None)
        p_content = request.POST.get("p_content", None)
        if id is None or id == "":
            Public.objects.create(p_title=p_title, p_content=p_content)
        else:
            public.p_title = p_title
            public.p_content = p_content

            public.save()

        return redirect("/public/list/")


@login_required
def PublicDel(request):
    id = request.GET.get("id")
    Public.objects.filter(id=id).delete()
    return redirect("/public/list")


@login_required
def PublicList(request):
    if request.method == "GET":
        if request.user.a_auth == 1:
            auth = AuthRelationAdmin.objects.filter(admin_id=request.user.id).filter(auth_id=2).first()
            if auth is None:
                return render(request, 'user_list.html', locals())
        auth = True
        page = request.GET.get("page")
        if page is None or page == "":
            page = 1

        keyword = request.GET.get("keyword", None)
        if keyword is not None and keyword != "":
            publicList = Public.objects.filter(p_title__contains=keyword).order_by("-id")
        else:
            publicList = Public.objects.order_by("-id")
        paginator = Paginator(publicList, 7)
        page = paginator.page(page)  # 传递当前页的实例对象到前端
    return render(request, 'public_list.html', locals())


# 维修管理
@login_required
def RepairOption(request):
    id = request.GET.get("id")
    repair = Repair.objects.filter(id=id).first()
    if request.method == "GET":
        if request.user.a_auth == 1:
            auth = AuthRelationAdmin.objects.filter(admin_id=request.user.id).filter(auth_id=2).first()
            if auth is None:
                return render(request, 'user_list.html', locals())
        auth = True
        return render(request, 'repairOption.html', locals())
    elif request.method == "POST":

        r_place = request.POST.get("r_place", None)
        r_phone = request.POST.get("r_phone", None)
        r_name = request.POST.get("r_name", None)
        r_status = request.POST.get("r_status", None)
        if id is None or id == "":
            Repair.objects.create(r_place=r_place, r_name=r_name, r_phone=r_phone, r_status=r_status)
        else:
            repair.r_place = r_place
            repair.r_name = r_name
            repair.r_phone = r_phone
            repair.r_status = r_status
            repair.save()

        return redirect("/repair/list/")


@login_required
def RepairtDel(request):
    id = request.GET.get("id")
    Repair.objects.filter(id=id).delete()
    return redirect("/repair/list")


@login_required
def RepairtList(request):
    if request.method == "GET":
        if request.user.a_auth == 1:
            auth = AuthRelationAdmin.objects.filter(admin_id=request.user.id).filter(auth_id=2).first()
            if auth is None:
                return render(request, 'user_list.html', locals())
        auth = True
        page = request.GET.get("page")
        if page is None or page == "":
            page = 1
        keyword = request.GET.get("keyword", None)
        if keyword is not None and keyword != "":
            repairList = Repair.objects.filter(r_name__contains=keyword).order_by("-id")
        else:
            repairList = Repair.objects.order_by("-id")
        paginator = Paginator(repairList, 7)
        page = paginator.page(page)  # 传递当前页的实例对象到前端
    return render(request, 'repair_list.html', locals())


@login_required
def ReportOption(request):
    id=request.GET.get("id")
    report=Report.objects.get(id=id)
    if request.method=="GET":
        return render(request,'reportOPtion.html',locals())
    else:
        content=request.POST.get("content")
        status=request.POST.get("status")
        report.feedback=content
        report.status=status
        report.save()
        return redirect("/report/list/")

# 业主问题上报表
@login_required
def ReportList(request):
    if request.method == "GET":
        if request.user.a_auth == 1:
            auth = AuthRelationAdmin.objects.filter(admin_id=request.user.id).filter(auth_id=2).first()
            if auth is None:
                return render(request, 'user_list.html', locals())
        auth = True
        page = request.GET.get("page")
        if page is None or page == "":
            page = 1
        keyword = request.GET.get("keyword", None)
        if keyword is not None and keyword != "":
            reportList = Report.objects.filter(r_content__contains=keyword).order_by("-id")
        else:
            reportList = Report.objects.order_by("-id")
        paginator = Paginator(reportList, 7)
        page = paginator.page(page)  # 传递当前页的实例对象到前端
    return render(request, 'report_list.html', locals())


# 投诉表

# Complaints


@login_required
def ComplaintsOption(request):
    id = request.GET.get("id")
    complaints = Complaints.objects.filter(id=id).first()
    homeowner = Homeowner.objects.all()
    if request.method == "GET":
        return render(request, 'complaintsOption.html', locals())
    elif request.method == "POST":

        h_account = request.POST.get("h_account", None)
        event = request.POST.get("event", None)
        r_name = request.POST.get("r_name", None)
        c_status = request.POST.get("c_status", None)
        homeowner = Homeowner.objects.get(id=h_account)
        if id is None or id == "":
            Complaints.objects.create(h_account=homeowner, event=event, c_status=c_status)
        else:
            complaints.h_account = homeowner
            complaints.event = event
            complaints.r_name = r_name
            complaints.c_status = c_status
            complaints.save()

        return redirect("/complaints/list/")


@login_required
def ComplaintsDel(request):
    id = request.GET.get("id")
    Complaints.objects.filter(id=id).delete()
    return redirect("/complaints/list")


@login_required
def ComplaintsList(request):
    if request.method == "GET":
        if request.user.a_auth == 1:
            auth = AuthRelationAdmin.objects.filter(admin_id=request.user.id).filter(auth_id=2).first()
            if auth is None:
                return render(request, 'user_list.html', locals())
        auth = True
        page = request.GET.get("page")
        if page is None or page == "":
            page = 1
        keyword = request.GET.get("keyword", None)
        if keyword is not None and keyword != "":
            ComplaintsList = Complaints.objects.filter(event__contains=keyword).order_by("-id")
        else:
            ComplaintsList = Complaints.objects.order_by("-id")
        paginator = Paginator(ComplaintsList, 7)
        page = paginator.page(page)  # 传递当前页的实例对象到前端
    return render(request, 'complaints_list.html', locals())


# 访客表


@login_required
def GuestOption(request):
    id = request.GET.get("id")
    guest = Guest.objects.filter(id=id).first()
    homeowner = Homeowner.objects.all()
    if request.method == "GET":
        return render(request, 'guestOption.html', locals())
    elif request.method == "POST":

        h_account = request.POST.get("h_account", None)
        g_phone = request.POST.get("g_phone", None)
        g_gname = request.POST.get("g_gname", None)
        g_gphone = request.POST.get("g_gphone", None)
        g_status = request.POST.get("g_status", None)
        homeowner = Homeowner.objects.get(id=h_account)

        if id is None or id == "":
            Guest.objects.create(h_account=homeowner, g_phone=g_phone, g_gname=g_gname, g_gphone=g_gphone,
                                 g_status=g_status)
        else:
            guest.h_account = homeowner
            guest.g_phone = g_phone
            guest.g_gname = g_gname
            guest.g_gphone = g_gphone
            guest.g_status = g_status
            guest.save()

        return redirect("/guest/list/")


@login_required
def GuestDel(request):
    id = request.GET.get("id")
    Guest.objects.filter(id=id).delete()
    return redirect("/guest/list")


@login_required
def GuestList(request):
    if request.method == "GET":
        if request.user.a_auth == 1:
            auth = AuthRelationAdmin.objects.filter(admin_id=request.user.id).filter(auth_id=2).first()
            if auth is None:
                return render(request, 'user_list.html', locals())
        auth = True
        page = request.GET.get("page")
        if page is None or page == "":
            page = 1
        keyword = request.GET.get("keyword", None)
        if keyword is not None and keyword != "":
            guestList = Guest.objects.filter(g_gname__contains=keyword).order_by("-id")
        else:
            guestList = Guest.objects.order_by("-id")
        paginator = Paginator(guestList, 7)
        page = paginator.page(page)  # 传递当前页的实例对象到前端
    return render(request, 'guest_list.html', locals())


# 修改管理员密码

def change_admin_password(request):
    if request.method == "GET":
        return render(request, 'password_change_admin.html')
    sparce = request.POST.get("sparce")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")
    if password1 != password2:
        msg = "两次密码不一致"
        return render(request, 'password_change_admin.html', locals())
    if request.user.a_sparce != sparce:
        msg = "密保不正确"
        return render(request, 'password_change_admin.html', locals())
    admin = Admin.objects.get(id=request.user.id)
    admin.set_password(password1)
    return redirect("/login")


def change_admin_sparce(request):
    if request.method == "GET":
        return render(request, 'sparce_change_admin.html')
    sparce = request.POST.get("sparce")
    password1 = request.POST.get("password1")

    user = authenticate(username=request.user.username,
                        password=password1)  # 类型为<class 'django.contrib.auth.models.User'>
    if user is not None:
        admin = Admin.objects.get(id=request.user.id)
        admin.a_sparce = sparce
        admin.save()
        msg2 = "修改成功"
    else:
        msg = "密码错误"
    return render(request, 'sparce_change_admin.html', locals())


def change_password1_for_admin(request):
    if request.method == "GET":
        return render(request, 'change_passwod1.html')
    if request.method == "POST":
        username = request.POST.get("username")
        sparce = request.POST.get("sparce")
        admin = Admin.objects.filter(username=username).first()
        if admin is None:
            msg = "该用户不存在"
            return render(request, 'change_passwod1.html', locals())
        if admin.a_sparce != sparce:
            msg = "密保不正确"
            return render(request, 'change_passwod1.html', locals())

        return render(request, 'change_passwod2.html', locals())


def change_password2_for_admin(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    admin = Admin.objects.filter(username=username).first()
    admin.set_password(password)
    return redirect("/login/")


# 公示大屏数据读取

def front_index(request):
    if request.COOKIES.get("id") is None:
        return redirect("/user/login")
    page = request.GET.get("page")
    if page is None or page == "":
        page = 1
    publicList = Public.objects.order_by("-id")
    paginator = Paginator(publicList, 7)
    page = paginator.page(page)  # 传递当前页的实例对象到前端
    if request.method == "GET":

        return render(request, 'index.html', locals())
    else:
        content = request.POST.get("content")
        homeowmer = Homeowner.objects.get(id=2)
        Report.objects.create(h_account=homeowmer, r_content=content)
        msg = "您提出的问题已经上报"
        return render(request, 'index.html', locals())


# 用户信息修改

# 用户登录，
def logoutUser(request):
    obj=redirect("/user/login/")
    obj.delete_cookie("id")
    obj.delete_cookie("username")
    obj.delete_cookie("avther")
    return obj
class LoginUserView(View):
    def get(self, request):
        hashkey = CaptchaStore.generate_key()  # 验证码答案
        image_url = captcha_image_url(hashkey)  # 验证码地址
        captcha = {'hashkey': hashkey, 'image_url': image_url}
        return render(request, 'uselogin.html', locals())

    def post(self, request):
        capt = request.POST.get("code", None)  # 用户提交的验证码
        key = request.POST.get("hashkey", None)  # 验证码答案
        username = request.POST.get("username", None)  # 验证码答案
        password = request.POST.get("password", None)  # 验证码答案
        hashkey = CaptchaStore.generate_key()  # 验证码答案
        image_url = captcha_image_url(hashkey)  # 验证码地址
        captcha = {'hashkey': hashkey, 'image_url': image_url}

        if self.jarge_captcha(capt, key) == False:
            msg = "验证码输入错误"
            return render(request, 'uselogin.html', locals())
        try:
            homeowner = Homeowner.objects.get(h_id=username)
        except Exception as e:
            print(e)
            msg = "该用户不存在"
            return render(request, 'uselogin.html', locals())
        if homeowner.h_password != password:
            msg = "密码错误"
            return render(request, 'uselogin.html', locals())

        obj = redirect("/index/")
        obj.set_cookie("is_login", True, 300000)  # cookie有效期为30秒
        obj.set_cookie("username", homeowner.h_name)
        obj.set_cookie("id", homeowner.id)
        obj.set_cookie("avther", homeowner.s_avther)
        return obj

    def jarge_captcha(self, captchaStr, captchaHashkey):
        if captchaStr and captchaHashkey:
            try:
                # 获取根据hashkey获取数据库中的response值
                get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
                if get_captcha.response == captchaStr.lower():  # 如果验证码匹配
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False

# 忘记密码


def change_password1_for_user(request):
    if request.method == "GET":
        return render(request, 'change_passwod_user1.html')
    if request.method == "POST":
        username = request.POST.get("username")
        sparce = request.POST.get("sparce")
        try:
            homeowner=Homeowner.objects.get(h_id=username)
        except:
            msg = "该证件号不存在"
            return render(request, 'change_passwod_user1.html', locals())
        if homeowner.h_sparce != sparce:
            msg = "密保不正确"
            return render(request, 'change_passwod_user1.html', locals())

        return render(request, 'change_passwod_user2.html', locals())


def change_password2_for_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    homeowner = Homeowner.objects.get(h_id=username)
    homeowner.h_password=password
    homeowner.save()
    return redirect("/user/login/")




# 用户密码修改
def change_user_password(request):
    if request.method == "GET":
        return render(request, 'password_change_user.html')
    sparce = request.POST.get("sparce")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")
    if password1 != password2:
        msg = "两次密码不一致"
        return render(request, 'password_change_user.html', locals())

    id=request.COOKIES["id"]
    homeowner=Homeowner.objects.get(id=id)
    if homeowner.h_sparce != sparce:
        msg = "密保不正确"
        return render(request, 'password_change_user.html', locals())
    homeowner.h_password=password1
    homeowner.save()
    return redirect("/login")

# 用户密保修改

def change_user_sparce(request):
    if request.method == "GET":
        return render(request, 'sparce_change_user.html')
    sparce = request.POST.get("sparce")
    password1 = request.POST.get("password1")
    id=request.COOKIES["id"]
    homeowner=Homeowner.objects.get(id=id)
    if homeowner.h_password!=password1:
        msg = "密码错误"
        return render(request, 'sparce_change_user.html', locals())

    homeowner.h_sparce = sparce
    homeowner.save()
    msg2 = "修改成功"

    return render(request, 'sparce_change_user.html', locals())

def change_user_profile(request):
    id=request.COOKIES["id"]

    homeowner=Homeowner.objects.get(id=id)

    if request.method == "GET":
        return render(request, 'profile_change_user.html',locals())

    h_phone = request.POST.get("h_phone")
    h_cname = request.POST.get("h_cname")
    h_cphone = request.POST.get("h_cphone")
    s_avther = request.FILES.get("s_avther")
    if s_avther is not None:
        with open("./static/images/"+s_avther.name,"wb") as f:
            for i in s_avther.chunks():
                f.write(i)
        homeowner.s_avther="/static/images/"+s_avther.name

    homeowner.h_phone = h_phone
    homeowner.h_cname = h_cname
    homeowner.h_cphone = h_cphone
    homeowner.save()
    msg = "修改成功"
    obj=redirect("/index/")
    obj.set_cookie("avther", "/static/images/"+s_avther.name)


    return obj