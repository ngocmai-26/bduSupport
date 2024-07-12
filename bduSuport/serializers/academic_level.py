from rest_framework.serializers import ModelSerializer
from ..models.academic_level import AcademicLevel

class AcademicLevelSerializer(ModelSerializer):
    class Meta: 
        model = AcademicLevel
        fields ="__all__"

    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(set(existing) - set(fields)):
            self.fields.pop(field, None)