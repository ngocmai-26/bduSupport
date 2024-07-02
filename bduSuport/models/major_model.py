from django.db import models

class Major(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    industryCode = models.CharField(max_length=255)
    targets = models.CharField(max_length=255)
    combination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    benchmark = models.CharField(max_length=255) 
    tuition = models.CharField(max_length=255)
    trainingLocation = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
