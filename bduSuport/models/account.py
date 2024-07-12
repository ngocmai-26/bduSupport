from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager

# Định nghĩa Enum cho trạng thái tài khoản
class AccountStatus(models.TextChoices):
    BLOCKED = "blocked"
    ACTIVATED = "activated"
    UNVERIFIED = "unverified"

class AccountRole(models.TextChoices):
    ADMIN = "admin"
    ROOT = "root"

class Account(AbstractBaseUser):
    class Meta:
        app_label = "bduSuport"
        db_table = "account"

    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, null=False)
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=AccountStatus.choices)
    role = models.CharField(max_length=20, choices=AccountRole.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "email"

    objects = BaseUserManager()