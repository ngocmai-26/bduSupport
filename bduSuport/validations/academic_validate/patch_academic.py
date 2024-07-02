import re
from rest_framework import serializers
from .create_academic import CreateAcademicValidator

class PatchAcademicValidator(CreateAcademicValidator):
    name = serializers.CharField(max_length=255, required=False)
    
    def validate(self, data):
     
        if not any(data.values()):
            raise serializers.ValidationError("At least one field must be provided for partial update.")
        return data