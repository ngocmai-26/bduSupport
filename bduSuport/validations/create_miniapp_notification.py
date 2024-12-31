from rest_framework import serializers

class CreateMiniappNotificationValidator(serializers.Serializer):
    content = serializers.CharField(max_length=255)