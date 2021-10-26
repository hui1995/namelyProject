from django.shortcuts import render, redirect
from . import models
from .forms import UserForm, RegisterForm
import hashlib







def index(request):
    user_id = request.session.get('user_id', None)
    haveLearn = models.AppointmentRecord.objects.filter(user_id_id=user_id).filter(status=1).first()
    haveLearn2 = models.AppointmentRecord.objects.filter(user_id_id=user_id).filter(status=0).first()

    return render(request, 'index.html', locals())


def login(request):

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())

    login_form = UserForm()
    return render(request, 'login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")


def hash_code(s, salt='class_login'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def center(request):
    pass
    return render(request, 'center.html')


import datetime


def inquire(request):
    campus = request.GET.get("campus", None)
    teachingbuilding = request.GET.get("teachingbuilding", None)
    dateS = request.GET.get("dateS")
    campusList = models.Campus.objects.all()
    teachingbuildinglist = models.Teachingbuilding.objects.all()
    if campus is None or campus == "":
        campus = campusList.first()
        if campus is not None:
            campus = campus.id
    if teachingbuilding is None or teachingbuilding == "":
        teachingbuilding = teachingbuildinglist.first()
        if teachingbuilding is not None:
            teachingbuilding = teachingbuilding.id

    foorlist = models.Foor.objects.filter(teachingbuilding_id=teachingbuilding).filter(campus_id=campus).all()

    today = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')

    if dateS is None:
        dateS = today
    return render(request, 'inquire.html', locals())


def rule(request):
    return render(request, 'rule.html')


def message(request):
    user = models.User.objects.get(id=request.session.get("user_id"))
    if request.method == "GET":
        return render(request, 'message.html', locals())
    name = request.POST.get("name")
    email = request.POST.get("email")
    sex = request.POST.get("sex")
    user.name = name
    user.email = email
    user.sex = sex
    user.save()
    return redirect("/message/")


def order(request):
    user_id = request.session.get('user_id', None)
    appointmentList = models.AppointmentRecord.objects.filter(user_id_id=user_id)
    return render(request, 'order.html', locals())


def violate(request):
    user_id = request.session.get('user_id', None)

    appointmentList = models.AppointmentRecord.objects.filter(user_id_id=user_id).filter(status__in=(3,4))

    return render(request, 'violate.html',locals())


def here(request):
    user_id = request.session.get('user_id', None)
    appointmentList = models.AppointmentRecord.objects.filter(user_id_id=user_id).filter(status=0)
    for i in appointmentList:
        i.status = 1
        i.save()
    return redirect("/index")


def nohere(request):
    user_id = request.session.get('user_id', None)
    type=request.GET.get("type")
    if type=="1":
        status=2
        appointmentList = models.AppointmentRecord.objects.filter(user_id_id=user_id).filter(status=1)
        for i in appointmentList:
            i.status = status
            i.save()
    else:
        today = datetime.datetime.today()

        appointmentList = models.AppointmentRecord.objects.filter(user_id_id=user_id).filter(status=0)
        for i in appointmentList:
            print(i.appoint_date)
            print(today)
            if str(i.appoint_date)!=str(today)[0:10]:
                print("----")
                i.status = 5
                i.save()
    return redirect("/index")


def appointmentView(request):
    user = models.User.objects.get(id=request.session.get("user_id"))
    date = request.GET.get("date")
    id = request.GET.get("id")
    foor = request.GET.get("foor")
    today = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    offset2 = datetime.timedelta(days=7)
    today2 = datetime.datetime.now()

    if user.lock_time is not None and (user.lock_time.strftime()+offset2)>today2:
        return redirect("/floor/?id=" + foor + "&date=" + date+"&msg=该账号已经锁住")
    elif user.lock_time is not None and (user.lock_time.strftime()+offset2)<today2:
        user.lock_time=None
        if user.count1>=3:
            user.count1=0
        if user.count2>=3:
            user.count2=0

        user.save()

    if today == date:
        app_type = 0
        offset = datetime.timedelta(seconds=30)
        appoint_date = (today2 + offset).strftime('%Y-%m-%d %H:%M:%S')


    else:
        app_type = 1
        appoint_date = date + " 09:00:00"

    models.AppointmentRecord.objects.create(seat_id=id, appoint_date=date, user_id=user, status=0,
                                            appoint_type=app_type, appoint_date_hour=appoint_date)
    return redirect("/floor/?id=" + foor + "&date=" + date)


def floor(request):
    id = request.GET.get("id")
    date = request.GET.get("date")
    msg=request.GET.get("msg")
    classRoomList = models.ClassRoom.objects.filter(foor_id=id)
    data = []
    longList = []
    for i in classRoomList:
        seatList = models.Seat.objects.filter(classRoom_id=i.id).order_by("name")
        if len(seatList) > len(longList):
            longList = seatList
        dict1 = {}
        dict1["name"] = i.name
        seatList2 = []
        for x in seatList:
            dict2 = {}
            dict2["name"] = x.name
            dict2["id"] = x.id
            haveUser = models.AppointmentRecord.objects.filter(appoint_date=date).filter(seat_id=x.id).filter(
                status__in=(0, 1)).first()
            if haveUser is not None:
                dict2['haveUser'] = True
            else:
                dict2["haveUser"] = False
            seatList2.append(dict2)
        dict1["seatList"] = seatList2
        data.append(dict1)
    return render(request, 'floor.html', locals())
