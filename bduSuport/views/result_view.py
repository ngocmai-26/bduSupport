from django.http import HttpResponse
from rest_framework import viewsets, permissions
from ..models.result_model import Result
from ..serializers.result_serializer import ResultSerializer
# Create your views here.

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    

def index(request):
    return HttpResponse("Hello My App")