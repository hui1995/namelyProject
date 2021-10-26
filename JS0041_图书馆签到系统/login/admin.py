from django.contrib import admin
from . import models
from login.models import AppointmentRecord,User,Teachingbuilding,Seat,ClassRoom,Campus,Foor
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Campus)
admin.site.register(models.Teachingbuilding)
admin.site.register(models.Seat)
admin.site.register(models.ClassRoom)
admin.site.register(models.Foor)
