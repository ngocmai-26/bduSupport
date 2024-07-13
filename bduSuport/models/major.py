from django.db import models
from django.core.validators import MinValueValidator

class Major(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    expected_target = models.CharField(max_length=255)
    college_exam_groups  = models.ManyToManyField()
    description = models.CharField(max_length=255)
    year = models.IntegerField(validators=[MinValueValidator(0)])
    benchmark = models.CharField(max_length=255) 
    tuition = models.CharField(max_length=255)
    training_location = models.CharField(max_length=255)