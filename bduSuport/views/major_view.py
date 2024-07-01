from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ..models.major_model import Major
from ..serializers.major_serializer import MajorSerializer

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
        serializer = MajorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'Major created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Error',
            'message': 'Failed to create major',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

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
            queryset = Major.objects.get(pk=pk)
        except Major.DoesNotExist:
            return Response({
                'status': 'Error',
                'message': 'Major not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = MajorSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'Major updated successfully',
                'data': serializer.data
            })
        return Response({
            'status': 'Error',
            'message': 'Failed to update major',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

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
