from django.db import models

class AcademicLevel(models.Model):
    name = models.CharField(max_length=255)