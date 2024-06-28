from rest_framework.serializers import ModelSerializer
from ..models.academic_level_model import AcademicLevel

class AcademicLevelSerializer(ModelSerializer):
    class Meta: 
        model = AcademicLevel
        fields = ['id', 'name']