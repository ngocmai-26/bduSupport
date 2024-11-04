from rest_framework import serializers

from bduSuport.models.academic_level import AcademicLevel
from bduSuport.models.training_location import TrainingLocation

class MajorsFilter(serializers.Serializer):
    year = serializers.IntegerField(required=False)
    academic_level = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=AcademicLevel.objects.filter(deleted_at=None)
    )
    training_location = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=TrainingLocation.objects.filter(deleted_at=None)
    )