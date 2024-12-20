from rest_framework import serializers
from bduSuport.models.training_location import TrainingLocation

class UpdateContactValidator(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=255)
    phone = serializers.CharField(required=False, max_length=20)
    location = serializers.PrimaryKeyRelatedField(
        required=False, 
        queryset=TrainingLocation.objects.filter(deleted_at=None)
    )