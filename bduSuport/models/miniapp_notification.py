from django.db import models

from bduSuport.models.mini_app_user import MiniAppUser

class MiniappNotification(models.Model):
    class Meta:
        db_table = "miniapp_notification"

    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=255)
    user = models.ForeignKey(MiniAppUser, on_delete=models.CASCADE, related_name="miniapp_notifications")
    read_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)