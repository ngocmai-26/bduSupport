from django.db import models

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    is_code = models.CharField(max_length=255, null=True)
    is_verified = models.CharField(max_length=255, null=True)
    
   