import re
from rest_framework import serializers

class CreateAccountValidator(serializers.Serializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=False)
    password = serializers.CharField(required=True)

    def validate_email(self, value):
        
        return value

    def validate_phone(self, value):
        
        phone_pattern = re.compile(r"^\+(?:[0-9] ?){6,14}[0-9]$")
        if not phone_pattern.match(value):
            raise serializers.ValidationError("Invalid phone number.")
        
        return value
    
    def validate_password(self, value):
        
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        if not re.search(r"[a-zA-Z]", value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError("Password must contain at least one number.")
        
        return value
    