from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.news_model import New
from ..serializers.new_serializer import NewSerializer
from PIL import Image
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
# Create your views here.

class NewViewSet(viewsets.ViewSet):
    filter_backends = [ SearchFilter, OrderingFilter]
    search_fields = ['title'] 
    ordering_fields = ['id', 'title', 'type']  

    def list(self, request):
        queryset = New.objects.all()
        search_query = request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = NewSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = NewSerializer(data=request.data)
        if serializer.is_valid():
            
            if 'image' in request.FILES:
                image = request.FILES['image']
                try:
                    img = Image.open(image)
                    img.verify()
                except (IOError, SyntaxError):
                    raise ValidationError({'image': 'Invalid image file'})
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            queryset = New.objects.get(pk=pk)
        except New.DoesNotExist:
            return Response({'detail': 'New object not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = NewSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            queryset = New.objects.get(pk=pk)
        except New.DoesNotExist:
            return Response({'detail': 'New object not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = NewSerializer(queryset, data=request.data)
        if serializer.is_valid():
            
            if 'image' in request.FILES:
                image = request.FILES['image']
                try:
                    img = Image.open(image)
                    img.verify()
                except (IOError, SyntaxError):
                    raise ValidationError({'image': 'Invalid image file'})
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            queryset = New.objects.get(pk=pk)
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except New.DoesNotExist:
            return Response({'detail': 'New object not found'}, status=status.HTTP_404_NOT_FOUND)