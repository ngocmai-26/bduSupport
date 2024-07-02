from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ..models.major_model import Major
from ..serializers.major_serializer import MajorSerializer
from bduSuport.validations.major_validate.create_major import CreateMajorValidator
from bduSuport.validations.major_validate.update_major import UpdateMajorValidator
from bduSuport.validations.major_validate.patch_major import PatchMajorValidator

class MajorViewSet(viewsets.ViewSet):

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['industryCode', 'year']  
    search_fields = ['name'] 
    ordering_fields = ['name', 'year'] 

    def list(self, request):
        queryset = Major.objects.all()

        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = MajorSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        validator = CreateMajorValidator(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = validator.validated_data
        major = Major(**validated_data)
        major.save()

        if not major.id:
            return Response({
                'status': 'Error',
                'message': 'Failed to create major: no ID assigned after saving'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = MajorSerializer(major)
        return Response({
            'status': 'Major created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            queryset = Major.objects.get(pk=pk)
        except Major.DoesNotExist:
            return Response({
                'status': 'Error',
                'message': 'Major not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = MajorSerializer(queryset)
        return Response({
            'status': 'Success',
            'data': serializer.data
        })

    def update(self, request, pk=None):
        try:
            major = Major.objects.get(pk=pk)
        except Major.DoesNotExist:
            return Response({
                'status': 'Error',
                'message': 'Major not found'
            }, status=status.HTTP_404_NOT_FOUND)

        validator = UpdateMajorValidator(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = validator.validated_data
        serializer = MajorSerializer(major, data=validated_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            'status': 'Major updated successfully',
            'data': serializer.data
        })
        
    def patch(self, request, pk=None):
        try:
            major = Major.objects.get(pk=pk)
        except Major.DoesNotExist:
            return Response({
                'status': 'Error',
                'message': 'Major not found'
            }, status=status.HTTP_404_NOT_FOUND)

        validator = PatchMajorValidator(data=request.data, partial=True)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = validator.validated_data
        serializer = MajorSerializer(major, data=validated_data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            'status': 'Major partially updated successfully',
            'data': serializer.data
        })

    def destroy(self, request, pk=None):
        try:
            queryset = Major.objects.get(pk=pk)
            queryset.delete()
            return Response({
                'status': 'Major deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except Major.DoesNotExist:
            return Response({
                'status': 'Error',
                'message': 'Major not found'
            }, status=status.HTTP_404_NOT_FOUND)
