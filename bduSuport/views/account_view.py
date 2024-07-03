from django.http import HttpResponse
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from bduSuport.validations.account_validate.create_account import CreateAccountValidator
from bduSuport.validations.account_validate.update_account import UpdateAccountValidator
from ..models.account_model import Account
from ..serializers.account_serializer import AccountSerializer

class AccountViewSet(viewsets.ViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['email']

    def list(self, request):
        queryset = Account.objects.all()

        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = AccountSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        validate = CreateAccountValidator(data=request.data)

        if not validate.is_valid():
            return Response(validate.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = validate.validated_data
        
        email = validated_data.get('email')
        
        if Account.objects.filter(email=email).exists():
            return Response({"message": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            account = Account(**validated_data)
            account.save() 
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if account.id is None:
            return Response({"error": "Failed to create account."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"message": "Account created successfully", "account_id": account.id}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            account = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(account)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        try:
            account = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        validate = UpdateAccountValidator(data=request.data)
        if not validate.is_valid():
            return Response(validate.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = validate.validated_data

        serializer = AccountSerializer(account, data=validated_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)
    
    
    def destroy(self, request, pk=None):
        try:
            account = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
