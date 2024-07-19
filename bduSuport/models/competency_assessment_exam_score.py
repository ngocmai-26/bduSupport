from django.db import models
from django.core.validators import MinValueValidator

from bduSuport.models.admission_registration import AdmissionRegistration

class CompetencyAssessmentExamScore(models.Model):
    class Meta:
        db_table = "competency_assessment_exam_score"

    id = models.AutoField(primary_key=True)
    admission_registration = models.ForeignKey(AdmissionRegistration, on_delete=models.CASCADE, related_name="competency_assessment_exam_score")
    score = models.IntegerField(validators=[MinValueValidator(0)])