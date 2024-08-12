from django.db import models

from bduSuport.models.account import Account

class BusinessRecruitment(models.Model):
    class Meta:
        db_table = "business_recruiment"

    id = models.AutoField(primary_key=True)
    business_name = models.CharField(max_length=255)
    post_url = models.URLField()
    job_title = models.CharField(max_length=255)
    summary = models.TextField()
    banner = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="business_recruiments")