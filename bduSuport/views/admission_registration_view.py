from django.http import HttpResponse
from rest_framework import viewsets, permissions
from ..models.admission_registration_model import AdmissionRegistration
from ..serializers.admission_registration_serializer import AdmissionRegistrationSerializer
# Create your views here.

class AdmissionRegistrationViewSet(viewsets.ModelViewSet):
    queryset = AdmissionRegistration.objects.all()
    serializer_class = AdmissionRegistrationSerializer
    

    

def index(request):
    return HttpResponse("Hello My App")