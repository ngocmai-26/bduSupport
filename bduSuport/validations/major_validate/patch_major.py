import re
from rest_framework import serializers
from .create_major import CreateMajorValidator

class PatchMajorValidator(CreateMajorValidator):
    name = serializers.CharField(max_length=255, required=False)
    industryCode = serializers.CharField(max_length=255, required=False)
    targets = serializers.CharField(max_length=255, required=False)
    combination = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(max_length=255, required=False)
    year = serializers.CharField(max_length=255, required=False)
    benchmark = serializers.CharField(max_length=255, required=False) 
    tuition = serializers.CharField(max_length=255, required=False)
    trainingLocation = serializers.CharField(max_length=255, required=False)
    
    def validate(self, data):
     
        if not any(data.values()):
            raise serializers.ValidationError("At least one field must be provided for partial update.")
        return data