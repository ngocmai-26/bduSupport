from rest_framework import serializers
from ..models.admission_registration import AdmissionRegistration

class AdmissionRegistrationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = AdmissionRegistration
        fields = "__all__"

    final_score = serializers.SerializerMethodField()
    is_passed = serializers.SerializerMethodField()

    def get_final_score(self, obj: AdmissionRegistration):
        return obj.final_score
    
    def get_is_passed(self, obj: AdmissionRegistration):
        return obj.is_passed