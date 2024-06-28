from django.http import HttpResponse
from rest_framework import viewsets, permissions
from ..models.evaluation_method_model import EvaluationMethod
from ..serializers.evaluation_method_serializer import EvaluationMethodSerializer
# Create your views here.

class EvaluationMethodViewSet(viewsets.ModelViewSet):
    queryset = EvaluationMethod.objects.all()
    serializer_class = EvaluationMethodSerializer

    

def index(request):
    return HttpResponse("Hello My App")