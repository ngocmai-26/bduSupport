from rest_framework import serializers

from bduSuport.models.academic_level import AcademicLevel

class MajorsFilter(serializers.Serializer):
    year = serializers.IntegerField(required=False)
    academic_level = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=AcademicLevel.objects.filter(deleted_at=None)
    )