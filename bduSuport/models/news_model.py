from django.db import models

class New(models.Model):
    title = models.CharField(max_length=255)
    link = models.TextField()
    type = models.IntegerField()
    image = models.ImageField(upload_to='news/%Y/%m', default=None)

