from rest_framework.serializers import ModelSerializer
from ..models.admission_registration_model import AdmissionRegistration

class AdmissionRegistrationSerializer(ModelSerializer):
    class Meta: 
        model = AdmissionRegistration
        fields = ['id', 'evaluationMethod', 'student']