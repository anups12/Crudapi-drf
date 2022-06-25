from django.contrib import admin
from . models import *
# Register your models here.

@admin.register(Course)
class CourseRegister(admin.ModelAdmin):
    list_display=('name','description', 'title')

@admin.register(Creator)
class CourseRegister(admin.ModelAdmin):
    list_display=('name','username')

@admin.register(Reader)
class CourseRegister(admin.ModelAdmin):
    list_display=('name','username')

@admin.register(Enrolled)
class CourseRegister(admin.ModelAdmin):
    list_display=('courses','user')