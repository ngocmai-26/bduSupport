from django.db import models

from bduSuport.models.college_exam_group import CollegeExamGroup
from bduSuport.models.subject import Subject

class CollegeM2MSubject(models.Model):
    class Meta:
        db_table = "college_m2m_subject"

    id = models.AutoField(primary_key=True)
    college_group = models.ForeignKey(CollegeExamGroup, on_delete=models.CASCADE, related_name="college_groups")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="subjects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)