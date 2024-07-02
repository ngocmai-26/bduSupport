from django.db import models

class New(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    link = models.TextField()
    type = models.IntegerField()
    image = models.ImageField(upload_to='news/%Y/%m', default=None)

