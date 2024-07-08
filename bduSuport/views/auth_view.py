from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
import secrets
import string
import jwt

# Import mô hình và Enum AccountStatus
from ..models.account_model import Account, AccountStatus
from ..validations.auth_validate.login_validate import LoginRequestValidator
from bduSuport.validations.account_validate.create_account import CreateAccountValidator
from ..validations.auth_validate.verify_validate import VerifyRequestValidator

class AuthView(viewsets.ViewSet):

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = LoginRequestValidator(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract the validated account object from the serializer
        account = serializer.validated_data['account']

        # Create JWT token
        payload = {
            'account_id': account.id,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        # Store token in cache
        cache.set(f"token_{account.id}", jwt_token, timeout=3600)

        return Response({"message": "Login successful", "token": jwt_token}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        validate = CreateAccountValidator(data=request.data)

        if not validate.is_valid():
            return Response(validate.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = validate.validated_data
        
        email = validated_data['email']  # Sử dụng email từ validated_data
        
        if Account.objects.filter(email=email).exists():
            return Response({"message": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            confirmation_code = ''.join(secrets.choice(string.digits) for _ in range(6))
            cache_key = f"account:{email}:verify_code"
            cache.set(cache_key, confirmation_code, timeout=900)  # Lưu với TTL = 15 phút
            
            subject = 'Confirmation Code for Registration'
            message = f'Your confirmation code is: {confirmation_code}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            send_mail(subject, message, from_email, recipient_list)
            
            # Tạo và lưu tài khoản với status mặc định là 'unverified'
            account = Account(**validated_data)
            account.save()

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"message": "Account created successfully. Confirmation code sent to your email.", "account_id": account.id}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], url_path='verify')
    def verify(self, request):
        validator = VerifyRequestValidator(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)

        email = validator.validated_data['email']
        otp = validator.validated_data['otp']
        account = validator.validated_data['account']

        cache_key = f"account:{email}:verify_code"
        cached_code = cache.get(cache_key)

        if not cached_code:
            return Response({"error": "Code expired or does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if otp != cached_code:
            return Response({"error": "Invalid code."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if account.status != AccountStatus.UNVERIFIED.value:
                return Response({"message": "Account already verified or not eligible for verification."}, status=status.HTTP_200_OK)

            account.status = AccountStatus.ACTIVATED.value
            account.save(update_fields=['status'])

            cache.delete(cache_key)

            return Response({"message": "Account verified successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)