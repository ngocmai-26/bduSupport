from rest_framework import serializers

from bduSuport.models.admission_registration import ReviewStatusChoices
from bduSuport.models.college_exam_group import CollegeExamGroup
from bduSuport.models.evaluation_method import EvaluationMethod
from bduSuport.models.major import Major

class ListAdmissionRegistrationFilter(serializers.Serializer):
    evaluation_method = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=EvaluationMethod.objects.filter(deleted_at=None)
    )
    major = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Major.objects.filter(deleted_at=None)
    )
    college_exam_group = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=CollegeExamGroup.objects.filter(deleted_at=None)
    )
    review_status = serializers.ChoiceField(required=False, choices=ReviewStatusChoices.choices)