from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ..models.academic_level_model import AcademicLevel
from ..serializers.academic_level_serializer import AcademicLevelSerializer
from bduSuport.validations.academic_validate.create_academic import CreateAcademicValidator
from bduSuport.validations.academic_validate.update_academic import UpdateAcademicValidator

class AcademicLevelViewSet(viewsets.ViewSet):
    # Thêm các filter backend
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['degree_type']  
    search_fields = ['name']  
    ordering_fields = ['name', 'degree_type']  

    def list(self, request):
        queryset = AcademicLevel.objects.all()

        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = AcademicLevelSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        validator = CreateAcademicValidator(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = validator.validated_data

        academic_level = AcademicLevel.objects.create(**validated_data)

        if not academic_level.id:
            return Response({'message': 'Failed to create academic level'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = AcademicLevelSerializer(academic_level)
        return Response({
            'status': 'Academic level created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            academic_level = AcademicLevel.objects.get(pk=pk)
        except AcademicLevel.DoesNotExist:
            return Response({
                'status': 'Error',
                'message': 'Academic level not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AcademicLevelSerializer(academic_level)
        return Response({
            'status': 'Success',
            'data': serializer.data
        })

    def update(self, request, pk=None):
        try:
            academic_level = AcademicLevel.objects.get(pk=pk)
        except AcademicLevel.DoesNotExist:
            return Response({
                'status': 'Error',
                'message': 'Academic level not found'
            }, status=status.HTTP_404_NOT_FOUND)

        validator = UpdateAcademicValidator(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = validator.validated_data

        serializer = AcademicLevelSerializer(academic_level, data=validated_data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            'status': 'Academic level updated successfully',
            'data': serializer.data
        })
        
    

    def destroy(self, request, pk=None):
        try:
            academic_level = AcademicLevel.objects.get(pk=pk)
            academic_level.delete()
            return Response({
                'status': 'Academic level deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except AcademicLevel.DoesNotExist:
            return Response({
                'status': 'Error',
                'message': 'Academic level not found'
            }, status=status.HTTP_404_NOT_FOUND)
