from django.db import models
from enum import Enum

class EvaluationMethods(Enum):
    HighSchoolGraduationExam = "high_school_graduation_exam"
    CompetencyAssessmentExam = "competency_assessment_exam"
    Grades_10_11_12 = "grades_10_11_12"
    Grade_12 = "grade_12"
    FiveSemestersOfHighSchool = "5_semesters_of_high_school"

class EvaluationMethod(models.Model):
    class Meta:
        db_table = "evaluation_method"

    code = models.CharField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    # create_by = models.IntegerField()



