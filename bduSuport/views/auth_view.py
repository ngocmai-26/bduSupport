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
from ..models.account import Account, AccountStatus
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