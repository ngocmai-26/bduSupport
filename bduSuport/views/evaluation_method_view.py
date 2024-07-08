from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ..models.evaluation_method_model import EvaluationMethod
from ..serializers.evaluation_method_serializer import EvaluationMethodSerializer
from bduSuport.validations.evaluation_method_validate.create_evaluation import CreateEvaluationValidator
from bduSuport.validations.evaluation_method_validate.update_evaluation import UpdateEvaluationValidator

class EvaluationMethodView(viewsets.ViewSet):
    def list(self, request):
        queryset = EvaluationMethod.objects.all()

        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = EvaluationMethodSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        validator = CreateEvaluationValidator(data=request.data)
        if not validator.is_valid():
            return Response({
                'status': 'Error',
                'message': 'Failed to create evaluation method',
                'errors': validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = validator.validated_data
        evaluation_method = EvaluationMethod.objects.create(**validated_data)
        
        if evaluation_method.id is None:
            return Response({
                'status': 'Error',
                'message': 'Failed to create evaluation method',
                'errors': {'id': 'ID was not assigned'}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = EvaluationMethodSerializer(evaluation_method)
        return Response({
            'status': 'Evaluation method created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

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

        validator = UpdateEvaluationValidator(data=request.data)
        if not validator.is_valid():
            return Response({
                'status': 'Error',
                'message': 'Failed to update evaluation method',
                'errors': validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        validated_data = validator.validated_data
        serializer = EvaluationMethodSerializer(evaluation_method, data=validated_data)
        if not serializer.is_valid():
            return Response({
                'status': 'Error',
                'message': 'Failed to update evaluation method',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            'status': 'Evaluation method updated successfully',
            'data': serializer.data
        })
        
    
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
