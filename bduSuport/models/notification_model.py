from django.db import models
from .account_model import Account

class Notification(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    trainingLocation = models.CharField(max_length=255)
    tuition = models.CharField(max_length=255)
    benchmark = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    image = models.ImageField(upload_to='notification/%Y/%m', default=None)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
  
  