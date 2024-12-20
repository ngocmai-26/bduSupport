from django.db import models

class Handbook(models.Model):
    class Meta:
        db_table = "handbook"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)