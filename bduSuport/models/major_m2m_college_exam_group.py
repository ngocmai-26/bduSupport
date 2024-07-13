from django.db import models

from bduSuport.models.college_exam_group import CollegeExamGroup
from bduSuport.models.major import Major

class MajorM2MCollegeExamGroup(models.Model):
    class Meta:
        db_table = "major_m2m_college_exam_group"

    id = models.AutoField(primary_key=True)
    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name="majors")
    college_exam_groups = models.ForeignKey(CollegeExamGroup, on_delete=models.CASCADE, related_name="college_exam_groups")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)