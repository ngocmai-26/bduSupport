from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models.students_model import Students
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from ..serializers.student_serializer import StudentsSerializer

class StudentsViewSet(viewsets.ModelViewSet):

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['major'] 
    search_fields = ['name', 'student_id'] 
    ordering_fields = ['name', 'year']  
    ordering = ['name']  
    
    
    def list(self, request):
        queryset = Students.objects.all()

        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = StudentsSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = StudentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Student created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Failed to create student.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            student = Students.objects.get(pk=pk)
            serializer = StudentsSerializer(student)
            return Response(serializer.data)
        except Students.DoesNotExist:
            return Response({
                "message": "Student not found."
            }, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            student = Students.objects.get(pk=pk)
        except Students.DoesNotExist:
            return Response({
                "message": "Student not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentsSerializer(student, data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response({
                "message": "Student updated successfully.",
                "data": serializer.data
            })
        return Response({
            "message": "Failed to update student.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            student = Students.objects.get(pk=pk)
            student.delete()
            return Response({
                "message": "Student deleted successfully."
            }, status=status.HTTP_204_NO_CONTENT)
        except Students.DoesNotExist:
            return Response({
                "message": "Student not found."
            }, status=status.HTTP_404_NOT_FOUND)
