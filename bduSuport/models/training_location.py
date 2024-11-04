from django.db import models

class TrainingLocation(models.Model):
    class Meta:
        db_table = "training_location"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)