from rest_framework import serializers

class CreateMediaValidator(serializers.Serializer):
    file = serializers.FileField()