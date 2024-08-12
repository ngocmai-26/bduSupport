from django.db import models

class MiniappRole(models.TextChoices):
    STUDENT = "student"
    PARENT = "parent"
    FORMER_STUDENT = "former_student"