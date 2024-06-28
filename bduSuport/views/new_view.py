from django.http import HttpResponse
from rest_framework import viewsets, permissions
from ..models.news_model import New
from ..serializers.new_serializer import NewSerializer
# Create your views here.

class NewViewSet(viewsets.ModelViewSet):
    queryset = New.objects.all()
    serializer_class = NewSerializer

    

def index(request):
    return HttpResponse("Hello My App")