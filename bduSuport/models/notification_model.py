from django.db import models
from .account_model import Account

class Notification(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    type = models.IntegerField(default=0)
    is_active = models.IntegerField(default=0)
    image = models.ImageField(upload_to='notification/%Y/%m', default=None)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
  
  