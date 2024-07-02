from django.db import models
from .admission_registration_model import AdmissionRegistration
from .students_model import Students
from .evaluation_method_model import EvaluationMethod

class Result(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=255)
    score = models.FloatField()
    student = models.ForeignKey(Students, on_delete=models.SET_NULL, null=True)
    evaluation_method = models.ForeignKey(EvaluationMethod, on_delete=models.SET_NULL, null=True)
    registration = models.ForeignKey(AdmissionRegistration, on_delete=models.SET_NULL, null=True)
    