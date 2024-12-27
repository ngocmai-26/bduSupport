from django.db import models
from bduSuport.models.account import Account

class BackofficeAuditLog(models.Model):
    class Meta:
        db_table = "backoffice_audit_log"
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="backoffice_audit_logs")
    action = models.CharField(max_length=255)
    detail = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)