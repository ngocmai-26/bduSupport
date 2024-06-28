from django.db import models
from .evaluation_method_model import EvaluationMethod
from .students_model import Students

class AdmissionRegistration(models.Model):
    evaluationMethod = models.ForeignKey(EvaluationMethod, on_delete=models.SET_NULL, null=True)  
    student = models.ForeignKey(Students, on_delete=models.SET_NULL, null=True)  
  