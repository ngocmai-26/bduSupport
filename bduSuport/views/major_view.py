from django.http import HttpResponse
from rest_framework import viewsets, permissions
from ..models.major_model import Major
from ..serializers.major_serializer import MajorSerializer
# Create your views here.

class MajorViewSet(viewsets.ModelViewSet):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer

    

def index(request):
    return HttpResponse("Hello My App")