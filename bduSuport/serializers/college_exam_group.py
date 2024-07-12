from rest_framework import serializers

from bduSuport.models.college_exam_group import CollegeExamGroup
from bduSuport.serializers.subject_serializer import SubjectSerializer

class CollegeExamGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeExamGroup
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(set(existing) - set(fields)):
            self.fields.pop(field, None)


    subjects = SubjectSerializer(many=True)