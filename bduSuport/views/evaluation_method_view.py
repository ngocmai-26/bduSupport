from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ..models.evaluation_method_model import EvaluationMethod
from ..serializers.evaluation_method_serializer import EvaluationMethodSerializer

class EvaluationMethodViewSet(viewsets.ViewSet):

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'year'] 
    search_fields = ['name'] 
    ordering_fields = ['name', 'year'] 

    def list(self, request):
        queryset = EvaluationMethod.objects.all()

        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = EvaluationMethodSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = EvaluationMethodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'Evaluation method created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Error',
            'message': 'Failed to create evaluation method',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            evaluation_method = EvaluationMethod.objects.get(pk=pk)
        except EvaluationMethod.DoesNotExist:
            return Response({
                'status': 'Error',
                'message': 'Evaluation method not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = EvaluationMethodSerializer(evaluation_method)
        return Response({
            'status': 'Success',
            'data': serializer.data
        })

    def update(self, request, pk=None):
        try:
            evaluation_method = EvaluationMethod.objects.get(pk=pk)
        except EvaluationMethod.DoesNotExist:
            return Response({
                'status': 'Error',
                'message': 'Evaluation method not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = EvaluationMethodSerializer(evaluation_method, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'Evaluation method updated successfully',
                'data': serializer.data
            })
        return Response({
            'status': 'Error',
            'message': 'Failed to update evaluation method',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            evaluation_method = EvaluationMethod.objects.get(pk=pk)
            evaluation_method.delete()
            return Response({
                'status': 'Evaluation method deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except EvaluationMethod.DoesNotExist:
            return Response({
                'status': 'Error',
                'message': 'Evaluation method not found'
            }, status=status.HTTP_404_NOT_FOUND)
