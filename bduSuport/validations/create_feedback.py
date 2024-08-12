from rest_framework import serializers

class CreateFeedbackValidator(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()