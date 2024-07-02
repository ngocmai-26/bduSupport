import re
from rest_framework import serializers
from .create_evaluation import CreateEvaluationValidator

class UpdateEvaluationValidator(CreateEvaluationValidator):
    name = serializers.CharField(max_length=255, required=False)