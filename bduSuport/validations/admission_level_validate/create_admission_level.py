import re
from rest_framework import serializers
from ...models.students_model import Students
from ...models.evaluation_method import EvaluationMethod

class CreateAdmissionValidator(serializers.Serializer):
    evaluationMethod = serializers.PrimaryKeyRelatedField(
        queryset=EvaluationMethod.objects.all(),
        allow_null=True,
        required=False
    )
    student = serializers.PrimaryKeyRelatedField(
        queryset=Students.objects.all(),
        allow_null=True,
        required=False
    )