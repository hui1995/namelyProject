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
    path("signup/",views.SignUpView),
    path("logout/",views.logoutAdmin),
    path("user/list/",views.userList),
    path("user/edit/",views.userEdit),
    path("user/del/",views.userDel),
    path("dept/list/",views.deptList),
    path("dept/del/",views.deptDel),
    path("dept/option/",views.deptOption),
    path("car/apply/list/",views.CarApplyList),
    path("car/apply/option/",views.CarApplyApply),
    path("car/list/",views.carList),
    path("car/option/",views.carOption),
    path("car/allocation/",views.carAllocation),
    path("car/del/",views.carDel),
    path("car/auth/list/",views.CarAuthList),
    path("car/auth/now/",views.CarAuthNow),
    path("car/apply/detail/",views.CarApplyDetail),
    path("car/option/list/",views.carOptionList),
    path("car/option/add/",views.carOptionAdd),
    path("",views.index),








]
