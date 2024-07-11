from rest_framework import serializers

class CreateMiniAppSessionValidator(serializers.Serializer):
    token = serializers.CharField(required=True)