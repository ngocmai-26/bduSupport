from rest_framework import serializers
from bduSuport.models.training_location import TrainingLocation

class CreateContactValidator(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20)
    location = serializers.PrimaryKeyRelatedField(
        queryset=TrainingLocation.objects.filter(deleted_at=None)
    )