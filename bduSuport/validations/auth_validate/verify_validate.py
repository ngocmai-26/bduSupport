import re
import bcrypt
from rest_framework import serializers
from django.core.cache import cache
from ...models.account_model import Account, AccountStatus


class VerifyRequestValidator(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)
    
    def validate_otp(self, value):
        # Kiểm tra định dạng OTP nếu cần (trong ví dụ này, giả sử OTP chỉ là chuỗi 6 chữ số)
        if not re.match(r'^\d{6}$', value):
            raise serializers.ValidationError("OTP must be a 6 digit number.")
        return value

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        # Kiểm tra sự tồn tại của tài khoản
        try:
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Account does not exist.")

        # Kiểm tra trạng thái tài khoản
        if account.status != AccountStatus.UNVERIFIED.value:
            raise serializers.ValidationError("Account is not eligible for verification.")

        # Kiểm tra OTP từ Redis
        cache_key = f"account:{email}:verify_code"
        cached_otp = cache.get(cache_key)

        if not cached_otp:
            raise serializers.ValidationError("OTP expired or does not exist.")
        if otp != cached_otp:
            raise serializers.ValidationError("Invalid OTP.")

        # Đưa account vào validated_data để sử dụng trong View
        data['account'] = account

        return data