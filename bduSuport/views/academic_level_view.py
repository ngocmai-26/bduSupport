from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ..models.academic_level_model import AcademicLevel
from ..serializers.academic_level_serializer import AcademicLevelSerializer

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
        serializer = AcademicLevelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'Academic level created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Error',
            'message': 'Failed to create academic level',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

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

        serializer = AcademicLevelSerializer(academic_level, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'Academic level updated successfully',
                'data': serializer.data
            })
        return Response({
            'status': 'Error',
            'message': 'Failed to update academic level',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

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
