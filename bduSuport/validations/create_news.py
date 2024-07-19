from rest_framework import serializers

from bduSuport.models.news import News

class CreateNewsValidator(serializers.ModelSerializer):
    class Meta:
        model = News
        exclude = ["author", "deleted_at"]

    image = serializers.ImageField()