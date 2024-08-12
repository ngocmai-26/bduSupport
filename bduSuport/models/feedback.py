from django.db import models

from bduSuport.models.account import Account

class Feedback(models.Model):
    class Meta:
        db_table = "feedback"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="feedbacks")