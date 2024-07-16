from django.db import models
from .evaluation_method import EvaluationMethod
from bduSuport.models.student import Student

class AdmissionRegistration(models.Model):
    id = models.AutoField(primary_key=True)
    evaluation_method = models.OneToOneField(EvaluationMethod, on_delete=models.SET_NULL, related_name="evaluation_method")  
    student = models.OneToOneField(Student, on_delete=models.SET_NULL, related_name="student")  
  