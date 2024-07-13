from rest_framework import serializers

from bduSuport.models.college_exam_group import CollegeExamGroup

class CreateMajorValidator(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    expected_target = serializers.IntegerField(min_value=0)
    college_exam_groups = serializers.PrimaryKeyRelatedField(
        queryset=CollegeExamGroup.objects.filter(deleted_at=None),
        many=True,
        allow_empty=False
    )
    description = serializers.CharField()
    year = serializers.IntegerField(min_value=0)
    benchmark_30 = serializers.DecimalField(max_digits=4, decimal_places=2, min_value=0, max_value=30)
    benchmark_competency_assessment_exam = serializers.IntegerField(min_value=0)
    tuition_fee = serializers.IntegerField(min_value=0)
    training_location = serializers.CharField()