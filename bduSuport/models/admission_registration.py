from django.db import models

from bduSuport.models.college_exam_group import CollegeExamGroup
from bduSuport.models.major import Major
from bduSuport.models.mini_app_user import MiniAppUser
from .evaluation_method import EvaluationMethod
from bduSuport.models.student import Student

class AdmissionRegistration(models.Model):
    class Meta:
        db_table = "admission_registration"

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(MiniAppUser, on_delete=models.CASCADE, related_name="admission_registrations")
    evaluation_method = models.ForeignKey(EvaluationMethod, on_delete=models.CASCADE, related_name="admission_registrations")  
    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name="admission_registrations")
    college_exam_group = models.ForeignKey(CollegeExamGroup, on_delete=models.CASCADE, related_name="admission_registrations")
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="admission_registration")
    created_at = models.DateTimeField(auto_now_add=True)
    recalled_at = models.DateTimeField(null=True)
  