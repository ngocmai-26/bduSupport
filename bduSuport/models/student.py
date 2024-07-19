from django.db import models
from .academic_level import AcademicLevel
from .major import Major

class Student(models.Model):
    class Meta:
        db_table = "student"
        
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=255)
    gender = models.BooleanField()
    date_of_birth = models.DateField()
    citizen_id = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    high_school = models.CharField(max_length=255)
   