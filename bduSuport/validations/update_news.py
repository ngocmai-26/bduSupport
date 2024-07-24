from rest_framework import serializers

from bduSuport.models.news_type import NewsType

class UpdateNewsValidator(serializers.Serializer):
    title = serializers.CharField(required=False)
    link = serializers.URLField(required=False)
    image = serializers.ImageField(required=False)
    type = serializers.PrimaryKeyRelatedField(
        required=False, 
        queryset=NewsType.objects.filter(deleted_at=None)
    )
