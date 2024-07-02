from django.http import JsonResponse
from rest_framework import viewsets, status, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from ..models.result_model import Result
from ..serializers.result_serializer import ResultSerializer
from bduSuport.validations.result_validate.create_result import CreateResultValidator
from bduSuport.validations.result_validate.update_result import UpdateResultValidator
from bduSuport.validations.result_validate.patch_result import PatchResultValidator

class ResultViewSet(viewsets.ModelViewSet):

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['student', 'subject', 'grade']  
    search_fields = ['student__name', 'subject__name'] 
    ordering_fields = ['grade', 'date'] 
    ordering = ['date'] 

    def list(self, request):
        queryset = Result.objects.all()

        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = ResultSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        validator = CreateResultValidator(data=request.data)
        if not validator.is_valid():
            return JsonResponse({
                'status': 'Error',
                'message': 'Failed to create result',
                'errors': validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        validated_data = validator.validated_data

        # Kiểm tra xem ID có tồn tại không và có trùng lặp không
        result_id = validated_data.get('id')
        if result_id is not None:
            if Result.objects.filter(id=result_id).exists():
                return JsonResponse({
                    'status': 'Error',
                    'message': 'Result with this ID already exists',
                    'errors': {'id': 'ID already exists'}
                }, status=status.HTTP_400_BAD_REQUEST)

        result = Result.objects.create(**validated_data)

        serializer = ResultSerializer(result)
        return JsonResponse({
            'status': 'Result created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            result = Result.objects.get(pk=pk)
            serializer = ResultSerializer(result)
            return JsonResponse(serializer.data)
        except Result.DoesNotExist:
            return JsonResponse({
                "message": "Result not found."
            }, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            result = Result.objects.get(pk=pk)
        except Result.DoesNotExist:
            return JsonResponse({
                "message": "Result not found."
            }, status=status.HTTP_404_NOT_FOUND)

        validator = UpdateResultValidator(data=request.data)
        if not validator.is_valid():
            return JsonResponse({
                'status': 'Error',
                'message': 'Failed to update result',
                'errors': validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        validated_data = validator.validated_data

        for key, value in validated_data.items():
            setattr(result, key, value)
        result.save()

        serializer = ResultSerializer(result)
        return JsonResponse({
            'status': 'Result updated successfully',
            'data': serializer.data
        })
        
    def patch(self, request, pk=None):
        try:
            result = Result.objects.get(pk=pk)
        except Result.DoesNotExist:
            return JsonResponse({
                "message": "Result not found."
            }, status=status.HTTP_404_NOT_FOUND)

        validator = PatchResultValidator(data=request.data)
        if not validator.is_valid():
            return JsonResponse({
                'status': 'Error',
                'message': 'Failed to patch result',
                'errors': validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        validated_data = validator.validated_data

        for key, value in validated_data.items():
            setattr(result, key, value)
        result.save()

        serializer = ResultSerializer(result)
        return JsonResponse({
            'status': 'Result patched successfully',
            'data': serializer.data
        })

    def destroy(self, request, pk=None):
        try:
            result = Result.objects.get(pk=pk)
            result.delete()
            return JsonResponse({
                "message": "Result deleted successfully."
            }, status=status.HTTP_204_NO_CONTENT)
        except Result.DoesNotExist:
            return JsonResponse({
                "message": "Result not found."
            }, status=status.HTTP_404_NOT_FOUND)
