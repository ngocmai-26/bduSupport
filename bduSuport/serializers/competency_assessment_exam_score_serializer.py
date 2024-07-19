from rest_framework import serializers

from bduSuport.models.competency_assessment_exam_score import CompetencyAssessmentExamScore

class CompetencyAssessmentExamScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetencyAssessmentExamScore
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(set(existing) - set(fields)):
            self.fields.pop(field, None)