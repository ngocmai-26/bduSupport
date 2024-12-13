from django.db import models

from bduSuport.models.app_function import AppFunction
from bduSuport.models.mini_app_user import MiniAppUser

class PersonalAppFunction(models.Model):
    class Meta:
        db_table = "personal_app_functions"
        unique_together = [
            ["app_function", "user"]
        ]

    id = models.AutoField(primary_key=True)
    app_function = models.ForeignKey(AppFunction, on_delete=models.CASCADE, related_name="personal_app_functions")
    user = models.ForeignKey(MiniAppUser, on_delete=models.CASCADE, related_name="personal_app_functions")
    is_show_in_home = models.BooleanField(default=True)