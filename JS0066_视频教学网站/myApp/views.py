from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.views import View
from myApp.models import User, Message, Comment, Comment2, Video, FileInfo, Message2
import json
from django.contrib.auth import authenticate, login, logout  # 登入和登出
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required  # 验证用户是否登录


def logoutAdmin(request):
    logout(request)
    return redirect("/login")

def home(request):
    return redirect("/login")

@login_required
def UserView(request):
    userlist = User.objects.filter(status__in=(0, 1))
    return render(request, 'userlist.html', locals())

@login_required
def delUser(request):
    id = request.GET.get("id")
    User.objects.get(id=id).delete()
    return redirect("/user/list/")

@login_required
def MessageView(request):
    messagelist = Message.objects.filter(teacherId=request.user.id)
    return render(request, 'messagelist.html', locals())

@login_required
def VideoView(request):
    videoList = Video.objects.filter(teacher=request.user)
    return render(request, 'videolist.html', locals())


from datetime import datetime

@login_required
def VideoAdd(request):
    id = request.GET.get("id")
    if id is not None:
        video = Video.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'videoAdd.html', locals())
    else:
        title = request.POST.get("title")
        image = request.FILES.get("image")
        videofile = request.FILES.get("video")

        if id is None:
            if videofile is None or image is None:
                msg = "封面图和视频不能为空"
                return render(request, 'videoAdd.html', locals())
            with open("./static/video/" + videofile.name, "wb") as f:
                for chunk in videofile.chunks():
                    f.write(chunk)

            Video.objects.create(title=title, video="/video/" + videofile.name, create_time=datetime.now(),
                                 teacher=request.user, pic="/images/" + image.name)
        else:
            video.title = title
            if videofile is not None:
                with open("./static/video/" + videofile.name, "wb") as f:
                    for chunk in videofile.chunks():
                        f.write(chunk)
                video.video = "/video/" + videofile.name
            if image is not None:
                with open("./static/images/" + image.name, "wb") as f:
                    for chunk in image.chunks():
                        f.write(chunk)
                video.pic = "/images/" + image.name
            video.save()
        return redirect("/video/list/")

@login_required
def delVideo(request):
    id = request.GET.get("id")
    Video.objects.get(id=id).delete()
    return redirect("/video/list/")

@login_required
def MessageAdd(request):
    id = request.GET.get("id")
    back = request.GET.get("back")
    message = Message.objects.get(id=id)
    messageChild= Message2.objects.filter(message=message).all()

    if request.method == "GET":
        return render(request, 'messageAdd.html', locals())
    replay = request.POST.get("replay")
    Message2.objects.create(replay=replay,message=message,replay_time=datetime.now(),user_id=request.user.id)
    message.replay = replay
    message.replay_time = datetime.now()
    message.save()
    if back =="me":
        return redirect("/me/message/list/")
    return redirect("/message/list/")

@login_required
def FileView(request):
    id = request.GET.get("id")
    fileList = FileInfo.objects.filter(video_id=id)
    return render(request, 'filelist.html', locals())


from datetime import datetime

@login_required
def FileAdd(request):
    id = request.GET.get("id")
    if request.method == "GET":
        return render(request, 'FileAdd.html', locals())
    else:
        title = request.POST.get("title")
        file = request.FILES.get("file")

        with open("./static/file/" + file.name, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        FileInfo.objects.create(title=title, file="/file/" + file.name, video_id=id)

        return redirect("/file/list/?id=" + id)

@login_required
def delFile(request):
    id = request.GET.get("id")
    fileid = request.GET.get("fileid")
    FileInfo.objects.get(id=id).delete()
    return redirect("/file/list/?id=" + fileid)


class SignUpView(View):
    def get(self, request):
        return render(request, 'signup.html', locals())

    def post(self, request):
        username = request.POST.get("username", None)  # 验证码答案
        password = request.POST.get("password", None)  # 验证码答案
        password2 = request.POST.get("password2", None)  # 验证码答案
        status = request.POST.get("status", None)  # 验证码答案
        if password != password2:
            msg = "两次输入密码不一致"
            return render(request, 'signup.html', locals())
        user = User.objects.filter(username=username).first()
        if user is not None:
            msg = "该用户已经存在"
            return render(request, 'signup.html', locals())
        user = User.objects.create_user(username, email=username + "@email.com", password=password)
        user.status = status
        user.save()
        return redirect("/login")


class LoginView(View):
    def get(self, request):

        return render(request, 'login.html', locals())

    def post(self, request):
        username = request.POST.get("username", None)  # 验证码答案
        password = request.POST.get("password", None)  # 验证码答案

        user = authenticate(username=username, password=password)  # 类型为<class 'django.contrib.auth.models.User'>
        #
        if user:
            login(request, user)  # 验证成功之后登录
            if user.status == 0:
                return redirect("/index")
            elif user.status==2:
                return redirect("user/list/")
            else:
                return redirect("/video/list/")
        else:
            msg = "账号或者密码不正确"
        return render(request, "login.html", locals())


#
@login_required
def indexforstud(request):
    video = Video.objects.all()
    return render(request, 'index.html', locals())


#
class VideoDetailView(View):
    def get(self, request):
        id = request.GET.get("id")
        video = Video.objects.get(id=id)
        filelist = FileInfo.objects.filter(video_id=id)
        comments = Comment.objects.filter(video_id=id).all()
        commentlist = []
        for i in comments:
            dict1 = {"main": i}
            comments2 = Comment2.objects.filter(comment=i).all()
            dict1["child"] = comments2
            commentlist.append(dict1)
        return render(request, 'videoDetail.html', locals())

    def post(self, request):
        id = request.GET.get("id")

        message = request.POST.get("message")
        Comment.objects.create(content=message, user=request.user, video_id=id, create_time=datetime.now())
        return redirect("/video/detail/?id=" + id)


@login_required
def addChildView(request):
    id = request.GET.get("id")
    message = request.POST.get("message")
    comment = Comment.objects.filter(id=id).first()
    Comment2.objects.create(user_id=request.user.id, content=message, comment_id=id, create_time=datetime.now())
    return redirect("/video/detail/?id=" + str(comment.video_id))


@login_required
def messageList(request):
    id = request.GET.get("id")
    user = User.objects.get(id=id)
    if request.method == "GET":
        return render(request, "my_message.html", locals())
    message = request.POST.get("message")

    Message.objects.create(content=message, teacherId=id, create_time=datetime.now(), stu=request.user)

    return redirect("/me/message/list/")


@login_required
def messageList2(request):
    if request.method == "GET":
        messageList = Message.objects.filter(stu=request.user).all()
        result=[]

        for i in messageList:
            dict1={}
            dict1["main"]=i
            dict1["user"]= User.objects.get(id=i.teacherId)

            dict1['child']=Message2.objects.filter(message=i).all()
            result.append(dict1)
        return render(request, "my_message2.html", locals())

