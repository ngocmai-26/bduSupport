from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models.students_model import Students
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from ..serializers.student_serializer import StudentsSerializer
from bduSuport.validations.student_validate.create_student import CreateStudentValidator
from bduSuport.validations.student_validate.update_student import UpdateStudentValidator
from bduSuport.validations.student_validate.patch_student import PatchStudentValidator

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
        validate = CreateStudentValidator(data=request.data)

        if not validate.is_valid():
            return Response({
                'status': 'Error',
                'message': 'Failed to create student',
                'errors': validate.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = validate.validated_data

        student = Students(**validated_data)
        student.save()

        if student.id is None:
            return Response({
                'status': 'Error',
                'message': 'Failed to create student: no ID assigned after saving'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = StudentsSerializer(student)
        return Response({
            'status': 'Success',
            'message': 'Student created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

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
                'status': 'Error',
                'message': 'Student not found'
            }, status=status.HTTP_404_NOT_FOUND)

        validate = UpdateStudentValidator(data=request.data)
        if not validate.is_valid():
            return Response({
                'status': 'Error',
                'message': 'Failed to update student',
                'errors': validate.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        validated_data = validate.validated_data

        serializer = StudentsSerializer(student, data=validated_data)
        if not serializer.is_valid():
            return Response({
                'status': 'Error',
                'message': 'Failed to update student',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            'status': 'Success',
            'message': 'Student updated successfully',
            'data': serializer.data
        })
        
    def patch(self, request, pk=None):
        try:
            student = Students.objects.get(pk=pk)
        except Students.DoesNotExist:
            return Response({
                'status': 'Error',
                'message': 'Student not found'
            }, status=status.HTTP_404_NOT_FOUND)

        validate = PatchStudentValidator(data=request.data, partial=True)
        if not validate.is_valid():
            return Response({
                'status': 'Error',
                'message': 'Failed to patch student',
                'errors': validate.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        validated_data = validate.validated_data

        serializer = StudentsSerializer(student, data=validated_data, partial=True)
        if not serializer.is_valid():
            return Response({
                'status': 'Error',
                'message': 'Failed to patch student',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            'status': 'Success',
            'message': 'Student patched successfully',
            'data': serializer.data
        })

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
