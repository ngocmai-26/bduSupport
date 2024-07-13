from django.db import models
from .academic_level import AcademicLevel
from .major import Major

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    fullName = models.CharField(max_length=255)
    gender = models.IntegerField(default=0)
    dateOfBirth = models.DateField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    highSchool = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    examGroup = models.CharField(max_length=255) 
    academicLevelId = models.ForeignKey(AcademicLevel, on_delete=models.SET_NULL, null=True)  
    major = models.ManyToManyField('Major',related_name="student")
   