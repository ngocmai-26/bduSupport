from rest_framework.serializers import ModelSerializer
from ..models.academic_level import AcademicLevel

class AcademicLevelSerializer(ModelSerializer):
    class Meta: 
        model = AcademicLevel
        fields ="__all__"