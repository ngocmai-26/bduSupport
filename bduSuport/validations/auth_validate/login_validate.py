import re
import bcrypt
from rest_framework import serializers
from ...models.account_model import Account


class LoginRequestValidator(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Check if user with this email exists
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Tài khoản với email này không tồn tại.")

        # Check password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise serializers.ValidationError("Mật khẩu không đúng.")

        # If validation passes, return the validated data
        data['user'] = user
        return data