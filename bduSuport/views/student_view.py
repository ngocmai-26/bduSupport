from django.http import HttpResponse
from rest_framework import viewsets, permissions
from ..models.students_model import Students
from ..serializers.student_serializer import StudentsSerializer
# Create your views here.

class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer

    

def index(request):
    return HttpResponse("Hello My App")