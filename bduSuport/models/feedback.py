from django.db import models

class Feedback(models.Model):
    class Meta:
        db_table = "feedback"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)