from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from bduSuport.models.admission_registration import AdmissionRegistration
from bduSuport.models.subject import Subject

class GradeChoices(models.IntegerChoices):
    GRADE_10 = 10
    GRADE_11 = 11
    GRADE_12 = 12
    GRADUATION = 0

class SemesterChoices(models.IntegerChoices):
    SCHOOL_YEAR = 0
    SEMESTER_1 = 1
    SEMESTER_2 = 2

class SubjectScore(models.Model):
    class Meta:
        db_table = "subject_score"

    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="subject_scores")
    admission_registration = models.ForeignKey(AdmissionRegistration, on_delete=models.CASCADE, related_name="subject_scores")
    score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    grade = models.IntegerField(choices=GradeChoices.choices)
    semester = models.IntegerField(choices=SemesterChoices.choices)