from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from bduSuport.models.academic_level import AcademicLevel
from bduSuport.models.college_exam_group import CollegeExamGroup
from bduSuport.models.evaluation_method import EvaluationMethod
from bduSuport.models.major import Major
from bduSuport.models.training_location import TrainingLocation

class CreateMajorValidator(serializers.Serializer):
    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Major.objects.filter(deleted_at=None),
                fields=['code', 'year', 'training_location']
            )
        ]

    code = serializers.CharField()
    name = serializers.CharField()
    expected_target = serializers.IntegerField(min_value=0)
    college_exam_groups = serializers.PrimaryKeyRelatedField(
        queryset=CollegeExamGroup.objects.filter(deleted_at=None),
        many=True,
        allow_empty=True,
    )
    description = serializers.CharField()
    year = serializers.IntegerField(min_value=0)
    benchmark_30 = serializers.FloatField(min_value=0.00, max_value=30.00)
    benchmark_school_record = serializers.FloatField(min_value=0.00, max_value=30.00)
    benchmark_competency_assessment_exam = serializers.IntegerField(min_value=0)
    tuition_fee = serializers.IntegerField(min_value=0)
    academic_level = serializers.PrimaryKeyRelatedField(queryset=AcademicLevel.objects.filter(deleted_at=None))
    evaluation_methods = serializers.PrimaryKeyRelatedField(
        queryset=EvaluationMethod.objects.filter(deleted_at=None), 
        many=True, 
        allow_empty=True,
    )
    number_of_credits = serializers.IntegerField(min_value=0)
    training_location = serializers.PrimaryKeyRelatedField(queryset=TrainingLocation.objects.filter(deleted_at=None))

    def validate(self, attrs):
        _attrs = super().validate(attrs)

        if not _attrs["academic_level"].need_evaluation_method:
            _attrs["evaluation_methods"] = []
            _attrs["college_exam_groups"] = []
            _attrs["benchmark_30"] = 0
            _attrs["benchmark_school_record"] = 0
            _attrs["benchmark_competency_assessment_exam"] = 0
        else:
            if len(_attrs["evaluation_methods"]) == 0:
                raise serializers.ValidationError("evaluation_methods_is_empty")
            
            if len(_attrs["college_exam_groups"]) == 0:
                raise serializers.ValidationError("college_exam_groups_is_empty")

        return _attrs
        
    
    def validate_benchmark_30(self, value: float):
        s = str(value)
        _, decimal_places = s.split(".")

        if len(decimal_places) > 2:
            raise serializers.ValidationError("invalid_benchmark_30_value")
        
        return value
    
    def validate_benchmark_school_record(self, value: float):
        s = str(value)
        _, decimal_places = s.split(".")

        if len(decimal_places) > 2:
            raise serializers.ValidationError("invalid_benchmark_school_record_value")
        
        return value