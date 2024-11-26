from rest_framework import serializers
import re

class ChangePasswordValidator(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_-])[A-Za-z\d@$!%_*?&-]{8,30}$', value):
            raise serializers.ValidationError("Mật khẩu không hợp lệ. Yêu cầu ít nhất 8 ký tự, bao gồm chữ cái viết thường, viết hoa, số và ký tự đặc biệt.")
        
        return value