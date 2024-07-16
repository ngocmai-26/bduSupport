from rest_framework import serializers

from bduSuport.models.academic_level import AcademicLevel
from bduSuport.models.college_exam_group import CollegeExamGroup
from bduSuport.models.evaluation_method import EvaluationMethod

class UpdateMajorValidator(serializers.Serializer):
    name = serializers.CharField(required=False)
    expected_target = serializers.IntegerField(required=False, min_value=0)
    college_exam_groups = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=CollegeExamGroup.objects.filter(deleted_at=None),
        many=True,
        allow_empty=False
    )
    description = serializers.CharField(required=False)
    year = serializers.IntegerField(required=False, min_value=0)
    benchmark_30 = serializers.FloatField(required=False, min_value=0.00, max_value=30.00)
    benchmark_competency_assessment_exam = serializers.IntegerField(required=False, min_value=0)
    tuition_fee = serializers.IntegerField(required=False, min_value=0)
    training_location = serializers.CharField(required=False)
    academic_level = serializers.PrimaryKeyRelatedField(queryset=AcademicLevel.objects.filter(deleted_at=None))
    evaluation_methods = serializers.PrimaryKeyRelatedField(queryset=EvaluationMethod.objects.filter(deleted_at=None), many=True, allow_empty=False)

    def validate_benchmark_30(self, value: float):
        s = str(value)
        _, decimal_places = s.split(".")

        if len(decimal_places) > 2:
            raise serializers.ValidationError("invalid_benchmark_30_value")
        
        return value