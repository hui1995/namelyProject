from django.contrib import admin

# Register your models here.
from .models import Course,CourseDetail,CourseStudent
 
# Register your models here.
admin.site.register(Course)
admin.site.register(CourseDetail)
admin.site.register(CourseStudent)