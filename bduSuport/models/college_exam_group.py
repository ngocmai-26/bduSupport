from django.db import models

from bduSuport.models.subject import Subject

class CollegeExamGroup(models.Model):
    class Meta:
        db_table = "college_exam_group"

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=255)
    subjects = models.ManyToManyField(Subject, through="bduSuport.CollegeM2MSubject", related_name="college_groups")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)