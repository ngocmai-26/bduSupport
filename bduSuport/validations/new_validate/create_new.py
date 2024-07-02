import re
from rest_framework import serializers

class CreateNewValidator(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=True)
    link = serializers.CharField(required=True)
    type = serializers.IntegerField(required=True)
    # image = serializers.ImageField(upload_to='news/%Y/%m', default=None)
    
    def validate_link(value):
        if not re.match(r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", value):
            raise serializers.ValidationError("Invalid URL format.")
        return value
    def validate_type(value):
        valid_types = ['news']
        if value not in valid_types:
            raise serializers.ValidationError(f"Type must be one of {valid_types}.")
        return value
    
   