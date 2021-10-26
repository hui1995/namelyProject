"""class URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from login import views

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^appointment/', views.appointmentView),
    url(r'^logout/', views.logout),
    url(r'^inquire/', views.inquire),
    url(r'^rule/', views.rule),
    url(r'^center/', views.center),
    url(r'^message/', views.message),
    url(r'^order/', views.order),
    url(r'^violate/', views.violate),
    url(r'^floor/', views.floor),
    url(r'^here/', views.here),
    url(r'^nohere/', views.nohere),
    url(r'^', views.index),

]
from login import models
import datetime
# 刷新签到未到

# @register_job(scheduler, "interval", seconds=3, id='test10')
def test_job2():
    now = datetime.datetime.now()

#
    appotmentRecorlist=models.AppointmentRecord.objects.filter(status=0)
    for i in appotmentRecorlist:
        if i.appoint_date_hour<now:
            i.status=3
            user=models.User.objects.get(id=i.user_id.id)
            user.count1+=1
            user.lock_time=datetime.datetime.now()
            user.save()
            i.save()

# 刷新签离

# @register_job(scheduler, 'cron', hour="23", minute='30',id='task_time')
def sched_2():
    appotmentRecorlist = models.AppointmentRecord.objects.filter(status=1)
    for i in appotmentRecorlist:
        i.status=4
        user = models.User.objects.get(id=i.user_id.id)
        user.count1 += 1
        user.lock_time = datetime.datetime.now()
        user.save()
        i.save()
register_events(scheduler)
scheduler.start()
print("Scheduler started!")
