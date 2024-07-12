from django.db import models

class EvaluationMethod(models.Model):
    class Meta:
        db_table = "evaluation_method"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    # create_by = models.IntegerField()



