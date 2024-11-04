from rest_framework import serializers

from bduSuport.models.training_location import TrainingLocation

class TrainingLocationFilter(serializers.Serializer):
    training_location = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=TrainingLocation.objects.filter(deleted_at=None)
    )