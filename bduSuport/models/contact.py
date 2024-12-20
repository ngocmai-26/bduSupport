from django.db import models
from bduSuport.models.training_location import TrainingLocation

class Contact(models.Model):
    class Meta:
        db_table = "contact"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    location = models.ForeignKey(TrainingLocation, on_delete=models.CASCADE, related_name="contacts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)