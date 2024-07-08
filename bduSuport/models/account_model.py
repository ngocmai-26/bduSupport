from django.db import models
from enum import Enum
import bcrypt

# Định nghĩa Enum cho trạng thái tài khoản
class AccountStatus(Enum):
    BLOCKED = 'blocked'
    ACTIVATED = 'activated'
    UNVERIFIED = 'unverified'

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    is_code = models.CharField(max_length=255, null=True)
    status = models.CharField(
        max_length=10,
        choices=[(status.value, status.name) for status in AccountStatus],
        default=AccountStatus.UNVERIFIED.value
    )

    class Meta:
        db_table = 'account'

    def save(self, *args, **kwargs):
        if not self.pk or 'password' in kwargs.get('update_fields', []):  # Mã hóa khi tạo mới hoặc cập nhật mật khẩu
            self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
