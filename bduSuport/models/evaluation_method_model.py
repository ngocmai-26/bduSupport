from django.db import models

class EvaluationMethod(models.Model):
    name = models.CharField(max_length=255)



