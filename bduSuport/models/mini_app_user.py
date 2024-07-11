from django.db import models

class MiniAppUser(models.Model):
    class Meta:
        db_table = "mini_app_user"
        
    id = models.AutoField(primary_key=True)
    mini_app_user_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    avatar_url = models.URLField()