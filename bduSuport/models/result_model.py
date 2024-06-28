from django.db import models

class Result(models.Model):
    subject = models.CharField(max_length=255)
    score = models.FloatField()
    password = models.CharField(max_length=255)
    