from rest_framework import serializers

class ReviewRegistrationValidator(serializers.Serializer):
    is_approve = serializers.BooleanField()