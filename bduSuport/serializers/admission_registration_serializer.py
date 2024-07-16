from rest_framework.serializers import ModelSerializer
from ..models.admission_registration import AdmissionRegistration

class AdmissionRegistrationSerializer(ModelSerializer):
    class Meta: 
        model = AdmissionRegistration
        fields = ['id', 'evaluationMethod', 'student']