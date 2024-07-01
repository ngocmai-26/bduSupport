import re
from rest_framework import serializers

class CreateAccountValidator(serializers.Serializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=False)
    password = serializers.CharField(required=True)

    def validate_phone(self, value):
        if not re.match(r"^\\+(?:[0-9] ?){6,14}[0-9]$", value):
            raise serializers.ValidationError("invalid_phone_number")
        
        return value
    