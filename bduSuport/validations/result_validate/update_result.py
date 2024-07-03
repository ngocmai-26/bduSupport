import re
from rest_framework import serializers
from ...models.students_model import Students
from ...models.evaluation_method_model import EvaluationMethod
from ...models.admission_registration_model import AdmissionRegistration

class UpdateResultValidator(serializers.Serializer):
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