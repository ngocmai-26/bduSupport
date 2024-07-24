from django.db import models

from bduSuport.models.account import Account
from bduSuport.models.news_type import NewsType

class News(models.Model):
    class Meta:
        db_table = "news"
        
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    link = models.URLField()
    image = models.URLField()
    type = models.ForeignKey(NewsType, on_delete=models.CASCADE, related_name="news")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="news")

