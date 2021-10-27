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
from myApp.views import LoginView

urlpatterns = [


    path("login/",LoginView.as_view()),
    path("logout/",views.logoutAdmin),
    path(r'captcha/', include('captcha.urls')),  # 这是生成验证码的图片
    path('refresh_captcha/', views.refresh_captcha),
    path('admin/list/', views.adminList),
    path('admin/add/', views.adminAdd),
    path('admin/edit/', views.adminEdit),
    path('admin/del/', views.adminDel),
    path('user/option/', views.UserOption),
    path('user/list/', views.userList),
    path('user/del/', views.userDel),
    path('staff/list/', views.staffList),
    path('staff/del/', views.staffDel),
    path('staff/option/', views.StaffOption),

    path('public/list/', views.PublicList),
    path('public/del/', views.PublicDel),
    path('public/option/', views.PublicOption),
    path('repair/list/', views.RepairtList),
    path('repair/del/', views.RepairtDel),
    path('repair/option/', views.RepairOption),

    path('complaints/list/', views.ComplaintsList),
    path('complaints/del/', views.ComplaintsDel),
    path('complaints/option/', views.ComplaintsOption),

    path('guest/list/', views.GuestList),
    path('report/list/', views.ReportList),
    path('report/edit/', views.ReportOption),
    path('guest/del/', views.GuestDel),
    path('guest/option/', views.GuestOption),

    path('admin/status/list/', views.adminStatusList),
    path('admin/change/password/', views.change_admin_password),
    path('admin/change/sparce/', views.change_admin_sparce),
    path('admin/status/change/', views.adminChangeStatus),
    path('admin/change/password1/', views.change_password1_for_admin),
    path('admin/change/password2/', views.change_password2_for_admin),
    path("admin/index/",views.index),
    path("user/login/",views.LoginUserView.as_view()),
    path("index/",views.front_index),

    path('user/change/password1/', views.change_password1_for_user),
    path('user/change/password2/', views.change_password2_for_user),
#     change_user_password

    path('user/change/password/', views.change_user_password),
    path('user/change/sparce/', views.change_user_sparce),
    path('user/change/profile/', views.change_user_profile),
    path('user/logout/', views.logoutUser),
    path("",views.homeView)







]
