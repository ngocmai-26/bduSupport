from rest_framework import serializers

class UpdateHandbookValidator(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=255)
    link = serializers.URLField(required=False, max_length=255)