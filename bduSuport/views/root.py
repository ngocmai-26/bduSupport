import random
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.conf import settings
from django.core.mail import send_mail

from bduSuport.services.otp import OtpService
from bduSuport.services.mail import EmailService

from bduSuport.middlewares.permissions.is_root import IsRoot
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication

from bduSuport.models.account import Account, AccountRole, AccountStatus
from bduSuport.validations.account_validate.create_account import CreateAccountValidator


class RootView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )
    permission_classes = (IsRoot, )

    @action(methods=["POST"], detail=False, url_path="accounts")
    @swagger_auto_schema(request_body=CreateAccountValidator)
    def create_account(self, request):
        try:
            validate = CreateAccountValidator(data=request.data)

            if not validate.is_valid():
                return Response(validate.errors, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = validate.validated_data
            
            if Account.objects.filter(email=validated_data["email"]).exists():
                return Response({"message": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
            
            _password: str = validated_data.pop("password")

            account = Account(**validated_data)
            account.set_password(_password)
            account.status = AccountStatus.UNVERIFIED
            account.role = AccountRole.ADMIN
            account.save() 
                
            if account.id is None:
                return Response({"error": "Failed to create account."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({"message": "Account created successfully", "account_id": account.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

