import re
from rest_framework import serializers

class UpdateEvaluationValidator(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)