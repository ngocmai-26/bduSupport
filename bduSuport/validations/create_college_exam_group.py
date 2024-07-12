from rest_framework import serializers

from bduSuport.models.subject import Subject

class CreateCollegeExamGroupValidator(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    subjects = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.filter(deleted_at=None),
        many=True,
        allow_empty=False
    )