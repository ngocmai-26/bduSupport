from rest_framework import serializers

class UpdateNewsValidator(serializers.Serializer):
    title = serializers.CharField(required=False)
    link = serializers.URLField(required=False)
    image = serializers.ImageField(required=False)
