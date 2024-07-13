from rest_framework.serializers import ModelSerializer

from bduSuport.serializers.college_exam_group import CollegeExamGroupSerializer
from ..models.major import Major

class MajorSerializer(ModelSerializer):
    class Meta: 
        model = Major
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(set(existing) - set(fields)):
            self.fields.pop(field, None)

    college_exam_groups = CollegeExamGroupSerializer(many=True)
       
    