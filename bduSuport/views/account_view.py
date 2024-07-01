from django.http import HttpResponse
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from ..models.account_model import Account
from ..serializers.account_serializer import AccountSerializer
from rest_framework.pagination import PageNumberPagination
from ..serializers.student_serializer import StudentsSerializer
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class AccountViewSet(viewsets.ViewSet):
    filter_backends = [ filters.SearchFilter]
    search_fields = ['email'] 


    def list(self, request):
        queryset = Account.objects.all()

        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = AccountSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            queryset = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(queryset)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        try:
            queryset = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            queryset = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    