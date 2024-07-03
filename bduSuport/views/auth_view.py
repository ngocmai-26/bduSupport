import bcrypt
import jwt
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
from django.core.cache import cache
from datetime import datetime, timedelta
from ..models.account_model import Account
from django.core.mail import send_mail

from bduSuport.validations.account_validate.create_account import CreateAccountValidator
import secrets
import string

class AuthViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response({"message": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        if not bcrypt.checkpw(password.encode('utf-8'), account.password.encode('utf-8')):
            return Response({"message": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            'account_id': account.id,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        cache.set(f"token_{account.id}", jwt_token, timeout=3600)

        return Response({"message": "Login successful", "token": jwt_token}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        validate = CreateAccountValidator(data=request.data)

        if not validate.is_valid():
            return Response(validate.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = validate.validated_data
        
        email = validated_data.get('email')
        
        if Account.objects.filter(email=email).exists():
            return Response({"message": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            confirmation_code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
            
            cache_key = f"confirmation_{email}"
            cache.set(cache_key, confirmation_code, timeout=3600) 
            
            subject = 'Confirmation Code for Registration'
            message = f'Your confirmation code is: {confirmation_code}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            send_mail(subject, message, from_email, recipient_list)
            
            # Update the account object with the confirmation code and save
            account = Account(**validated_data)
            account.is_code = confirmation_code
            account.save()
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"message": "Account created successfully. Confirmation code sent to your email.", "account_id": account.id}, status=status.HTTP_201_CREATED)
    @action(detail=False, methods=['post'], url_path='verified')
    def verified_email(self, request):
        email = request.data.get('email')
        is_code = request.data.get('is_code')
        
        if not email or not is_code:
            return Response({"error": "Email and code are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        cache_key = f"confirmation_{email}"
        cached_code = cache.get(cache_key)
        
        if not cached_code:
            return Response({"error": "Code expired or does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        if is_code != cached_code:
            return Response({"error": "Invalid code."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            account = Account.objects.get(email=email)
            
            if account.is_verified:
                return Response({"message": "Account already verified."}, status=status.HTTP_200_OK)
            
            account.is_verified = True
            account.save()
            
            cache.delete(cache_key)
            
            return Response({"message": "Code verified successfully."}, status=status.HTTP_200_OK)
        
        except Account.DoesNotExist:
            return Response({"error": "Account does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
