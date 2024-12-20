from rest_framework import serializers

class CreateHandbookValidator(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    link = serializers.URLField(max_length=255)