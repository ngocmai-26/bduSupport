from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Định nghĩa Enum cho trạng thái tài khoản
class AccountStatus(models.TextChoices):
    BLOCKED = "blocked"
    ACTIVATED = "activated"
    UNVERIFIED = "unverified"

class AccountRole(models.TextChoices):
    ADMIN = "admin"
    NORMAL = "normal"

class Account(AbstractBaseUser):
    class Meta:
        app_label = "bduSuport"
        db_table = "account"

    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=AccountStatus.choices)
    role = models.CharField(max_length=20, choices=AccountRole.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "email"