from rest_framework import serializers

class UpdateAcademicLevelValidator(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=255)
    need_evaluation_method = serializers.BooleanField(required=False)