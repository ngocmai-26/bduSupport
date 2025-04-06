from rest_framework import serializers

from bduSuport.models.academic_level import AcademicLevel
from bduSuport.models.training_location import TrainingLocation

class MajorsFilter(serializers.Serializer):
    year = serializers.IntegerField(required=False)
    open_to_recruitment = serializers.BooleanField(required=False)
    academic_level = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=AcademicLevel.objects.filter(deleted_at=None)
    )
    training_location = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=TrainingLocation.objects.filter(deleted_at=None)
    )

    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(set(existing) - set(fields)):
            self.fields.pop(field, None)