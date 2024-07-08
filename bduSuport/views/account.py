import random
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.core.cache import cache
from django.conf import settings
from django.core.mail import send_mail

from bduSuport.validations.account_validate.create_account import CreateAccountValidator
from bduSuport.validations.auth_validate.verify_validate import VerifyRequestValidator
from ..models.account import Account, AccountRole, AccountStatus
from ..serializers.account_serializer import AccountSerializer

from drf_yasg.utils import swagger_auto_schema

class AccountView(viewsets.ViewSet):
    def list(self, request):
        queryset = Account.objects.all()

        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = AccountSerializer(paginated_queryset, many=True, exclude=["password"])
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=CreateAccountValidator)
    def create(self, request):
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
            account.role = AccountRole.NORMAL
            account.save() 
                
            if account.id is None:
                return Response({"error": "Failed to create account."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            otp = self.__generate_verify_otp(account.email)
            self.__send_otp_mail(account.email, otp)

            return Response({"message": "Account created successfully", "account_id": account.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def __generate_verify_otp(self, email: str):
            otp = str(random.randint(100000, 999999))
            cache.set(f"account:{email}:otp:{otp}", email, 15*60)
            return otp
    
    def __check_otp(self, email: str, otp:str) -> bool:
        return cache.get(f"account:{email}:otp:{otp}") is not None
    
    def __send_otp_mail(self, email, otp):
        try:
            subject = 'Confirmation Code for Registration'
            message = f'Your confirmation code is: {otp}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print(e)
        
    def retrieve(self, request, pk=None):
        try:
            account = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(account)
        return Response(serializer.data)
    
    @action(methods=["POST"], detail=False, url_path="verify")
    @swagger_auto_schema(request_body=VerifyRequestValidator)
    def verify_account(self, request):
        try:
            validate = VerifyRequestValidator(data=request.data)

            if not validate.is_valid():
                return Response(validate.errors, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = validate.validated_data
            email = validated_data["email"]
            otp = validated_data["otp"]
            
            if not self.__check_otp(email, otp):
                return Response({"message": "Verification failed!"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                account = Account.objects.get(email=email)
                
                if account.status != AccountStatus.UNVERIFIED:
                    return Response({"message": "Invalid account status!"}, status=status.HTTP_400_BAD_REQUEST) 
            
                account.status = AccountStatus.ACTIVATED
                account.save(update_fields=["status"])

                return Response(status=status.HTTP_200_OK)
            except:
                return Response(validate.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

