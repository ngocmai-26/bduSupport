from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    def __str__(self):
        return self.username


class AcademicLevel(models.Model):
    name = models.CharField(max_length=255)
    
class EvaluationMethod(models.Model):
    name = models.CharField(max_length=255)

class Students(models.Model):
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
   
class AdmissionRegistration(models.Model):
    evaluationMethod = models.ForeignKey(EvaluationMethod, on_delete=models.SET_NULL, null=True)  
    student = models.ForeignKey(Students, on_delete=models.SET_NULL, null=True)  
  
    
class Result(models.Model):
    subject = models.CharField(max_length=255)
    score = models.FloatField()
    password = models.CharField(max_length=255)
    
class Major(models.Model):
    name = models.CharField(max_length=255)
    industryCode = models.CharField(max_length=255)
    targets = models.CharField(max_length=255)
    combination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    benchmark = models.CharField(max_length=255) 
    tuition = models.CharField(max_length=255)
    trainingLocation = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Account(models.Model):
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    
   
        

class Notification(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    trainingLocation = models.CharField(max_length=255)
    tuition = models.CharField(max_length=255)
    benchmark = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    image = models.ImageField(upload_to='notification/%Y/%m', default=None)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
  
  
class New(models.Model):
    title = models.CharField(max_length=255)
    link = models.TextField()
    type = models.IntegerField()
    image = models.ImageField(upload_to='news/%Y/%m', default=None)

