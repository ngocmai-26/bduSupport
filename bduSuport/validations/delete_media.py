from rest_framework import serializers

class DeleteMediaValidator(serializers.Serializer):
    url = serializers.URLField()