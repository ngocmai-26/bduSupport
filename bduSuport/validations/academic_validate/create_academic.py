import re
from rest_framework import serializers

class CreateAcademicValidator(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True)
    
    def validate_name(self, value):
        
        if not re.match(r'^[\w\s\p{L}\p{M}]+$', value):
            raise serializers.ValidationError("Name must only contain alphanumeric characters and spaces.")
        return value