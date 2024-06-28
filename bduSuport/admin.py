from django.contrib import admin
from django.utils.html import mark_safe
from django import forms
from .models import Students, AdmissionRegistration, Result, Major, Account, Notification, New, AcademicLevel, EvaluationMethod

from django.urls import path


# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    class Media:
        pass
     
    
    list_filter = ['gender']
    search_fields=['fullName'] #Tìm trên trường subject của khóa ngoại course
    list_display = ['id', 'fullName', 'gender', 'phone', 'address']
  
class MajorAdmin(admin.ModelAdmin):
    class Media:
        pass
     
    
    list_filter = ['year']
    search_fields=['name'] #Tìm trên trường subject của khóa ngoại course
    list_display = ['id', 'name', 'industryCode', 'targets', 'combination']
  



admin.site.register(AcademicLevel)
admin.site.register(EvaluationMethod)
admin.site.register(Students, StudentAdmin)
admin.site.register(AdmissionRegistration)
admin.site.register(Result)
admin.site.register(Major, MajorAdmin)
admin.site.register(Account)
admin.site.register(Notification)
admin.site.register(New)


