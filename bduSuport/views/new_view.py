from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.news_model import New
from ..serializers.new_serializer import NewSerializer
from PIL import Image
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from bduSuport.validations.new_validate.create_new import CreateNewValidator
from bduSuport.validations.new_validate.update_new import UpdateNewValidator
# Create your views here.

class NewView(viewsets.ViewSet):
    def list(self, request):
        queryset = New.objects.all()
        search_query = request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = NewSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create_new(self, request):
        validator = CreateNewValidator(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # validator.validate_image(request.FILES)

        validated_data = validator.validated_data
        new_instance = New(**validated_data)
        
        if new_instance.id is None:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = NewSerializer(new_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            queryset = New.objects.get(pk=pk)
        except New.DoesNotExist:
            return Response({'detail': 'New object not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = NewSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            instance = New.objects.get(pk=pk)
        except New.DoesNotExist:
            return Response({'detail': 'New object not found'}, status=status.HTTP_404_NOT_FOUND)

        validator = UpdateNewValidator(instance, data=request.data, partial=True)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # validator.validate_image(request.FILES)

        validated_data = validator.validated_data
        serializer = NewSerializer(instance, data=validated_data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data)

    
    def destroy(self, request, pk=None):
        try:
            queryset = New.objects.get(pk=pk)
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except New.DoesNotExist:
            return Response({'detail': 'New object not found'}, status=status.HTTP_404_NOT_FOUND)