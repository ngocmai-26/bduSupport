from django.db import models
from bduSuport.models.mini_app_user import MiniAppUser

class StudentSupervisionRegistration(models.Model):
    class Meta:
        db_table = "student_supervision_registration"

    id = models.AutoField(primary_key=True)
    miniapp_user = models.ForeignKey(MiniAppUser, on_delete=models.CASCADE, related_name="student_supervision_registrations")
    student_dw_code = models.IntegerField(null=False)
    student_full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True )