from rest_framework import serializers

from bduSuport.serializers.college_exam_group import CollegeExamGroupSerializer
from bduSuport.serializers.evaluation_method_serializer import EvaluationMethodSerializer
from ..models.major import Major

class MajorSerializer(serializers.ModelSerializer):
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
    evaluation_methods = EvaluationMethodSerializer(many=True)
    academic_level_name = serializers.SerializerMethodField()

    def get_academic_level_name(self, obj: Major):
        return obj.academic_level.name
       
    