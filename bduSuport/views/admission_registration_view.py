from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ..models.admission_registration_model import AdmissionRegistration
from ..serializers.admission_registration_serializer import AdmissionRegistrationSerializer

class AdmissionRegistrationView(viewsets.ViewSet):
    def list(self, request):
        queryset = AdmissionRegistration.objects.all()

        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = AdmissionRegistrationSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = AdmissionRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'Error',
                'message': 'Failed to create admission registration',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({
            'status': 'Admission registration created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            admission_registration = AdmissionRegistration.objects.get(pk=pk)
        except AdmissionRegistration.DoesNotExist:
            return Response({
                'status': 'Error',
                'message': 'Admission registration not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AdmissionRegistrationSerializer(admission_registration)
        return Response({
            'status': 'Success',
            'data': serializer.data
        })

    def update(self, request, pk=None):
        try:
            admission_registration = AdmissionRegistration.objects.get(pk=pk)
        except AdmissionRegistration.DoesNotExist:
            return Response({
                'status': 'Error',
                'message': 'Admission registration not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AdmissionRegistrationSerializer(admission_registration, data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'Error',
                'message': 'Failed to update admission registration',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            'status': 'Admission registration updated successfully',
            'data': serializer.data
        })
        
   
    def destroy(self, request, pk=None):
        try:
            admission_registration = AdmissionRegistration.objects.get(pk=pk)
            admission_registration.delete()
            return Response({
                'status': 'Admission registration deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except AdmissionRegistration.DoesNotExist:
            return Response({
                'status': 'Error',
                'message': 'Admission registration not found'
            }, status=status.HTTP_404_NOT_FOUND)
