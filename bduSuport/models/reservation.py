from django.db import models
from bduSuport.models.mini_app_user import MiniAppUser
from bduSuport.models.major import Major
from bduSuport.const.provinces import vietnam_provinces

class Reservation(models.Model):
    class Meta:
        db_table = "reservation"

    id = models.AutoField(primary_key=True)
    miniapp_user = models.ForeignKey(MiniAppUser, on_delete=models.CASCADE, related_name="reservations")
    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name="reservations")
    full_name = models.CharField(max_length=255)
    birthday = models.DateTimeField()
    school_name = models.CharField(max_length=255)
    class_name = models.CharField(max_length=50)
    province = models.CharField(max_length=100, choices=[(key, value) for key, value in vietnam_provinces.items()])
    phone_number = models.CharField(max_length=15)
    zalo_phone_number = models.CharField(max_length=15)
    citizen_id_card = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)