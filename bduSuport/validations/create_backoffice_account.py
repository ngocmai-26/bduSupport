import re
from rest_framework import serializers


class CreateBackofficeAccountValidator(serializers.Serializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=False)
    password = serializers.CharField(required=True)

    def validate_phone_number(self, value):
        phone_pattern = re.compile(r"^(?:\+)?[0-9]{6,14}$")
        if not phone_pattern.match(value):
            raise serializers.ValidationError("Invalid phone number!")
        
        return value
    
    def validate_password(self, value):
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_-])[A-Za-z\d@$!%_*?&-]{8,30}$', value):
            raise serializers.ValidationError("Mật khẩu không hợp lệ. Yêu cầu ít nhất 8 ký tự, bao gồm chữ cái viết thường, viết hoa, số và ký tự đặc biệt.")
        
        return value