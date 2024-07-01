from django.http import JsonResponse
from rest_framework import viewsets, status, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from ..models.result_model import Result
from ..serializers.result_serializer import ResultSerializer

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
        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

        serializer = ResultSerializer(result, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
