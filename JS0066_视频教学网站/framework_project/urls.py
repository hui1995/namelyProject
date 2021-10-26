"""framework_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path,include
from myApp import views
from myApp.views import LoginView,SignUpView

urlpatterns = [


    path("login/",LoginView.as_view()),
    path("signup/",SignUpView.as_view()),
    path("logout/",views.logoutAdmin),
    path("user/list/",views.UserView),
    path("user/del/",views.delUser),
    path("message/list/",views.MessageView),
    path("video/list/",views.VideoView),
    path("video/add/",views.VideoAdd),
    path("video/del/",views.delVideo),
    path("file/list/",views.FileView),
    path("file/add/",views.FileAdd),
    path("file/del/",views.delFile),
    path("index/",views.indexforstud),
    path("video/detail/",views.VideoDetailView.as_view()),
    path('add/comment/', views.addChildView),
    path('me/message/', views.messageList),
    path('message/add/', views.MessageAdd),
    path('me/message/list/', views.messageList2),
    path('', views.home),


]
