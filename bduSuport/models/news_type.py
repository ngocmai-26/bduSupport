from django.db import models

from bduSuport.models.account import Account

class NewsType(models.Model):
    class Meta:
        db_table = "news_type"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="news_types")