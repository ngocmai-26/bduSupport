from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from ..models.academic_level_model import AcademicLevel
from ..serializers.academic_level_serializer import AcademicLevelSerializer
# Create your views here.

class AcademicLevelViewSet(viewsets.ModelViewSet):
    queryset = AcademicLevel.objects.all()
    serializer_class = AcademicLevelSerializer

    

def index(request):
    return HttpResponse("Hello My App")
