import re
from rest_framework import serializers
from ...models.students_model import Students
from ...models.evaluation_method_model import EvaluationMethod
from ...models.admission_registration_model import AdmissionRegistration

class CreateResultValidator(serializers.Serializer):
    subject = serializers.CharField(max_length=255, required=True)
    score = serializers.FloatField(required=True)
    student = serializers.PrimaryKeyRelatedField(
        queryset=Students.objects.all(), 
        allow_null=False
    )
    evaluation_method = serializers.PrimaryKeyRelatedField(
        queryset=EvaluationMethod.objects.all(), 
        allow_null=False
    )
    registration = serializers.PrimaryKeyRelatedField(
        queryset=AdmissionRegistration.objects.all(), 
        allow_null=False
    )
    
    def validate_subject(self, value):
        if not re.match(r'^[A-Za-z0-9\s]+$', value):
            raise serializers.ValidationError("Subject name contains invalid characters.")
        return value

    def validate_score(self, value):
        if not (0.0 <= value <= 100.0):
            raise serializers.ValidationError("Score must be between 0.0 and 100.0.")
        return value

    