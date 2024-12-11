from django.db import models
from django.core.validators import MinValueValidator

class AppFunction(models.Model):
    class Meta:
        db_table = "app_functions"
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    icon_url = models.URLField(max_length=255)
    is_show = models.BooleanField(default=True)
    order = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    direct_to = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)