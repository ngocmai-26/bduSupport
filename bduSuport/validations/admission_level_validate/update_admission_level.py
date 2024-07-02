import re
from rest_framework import serializers
from ...models.students_model import Students
from ...models.evaluation_method_model import EvaluationMethod
from .create_admission_level import CreateAdmissionValidator

class UpdateAdmissionValidator(CreateAdmissionValidator):
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