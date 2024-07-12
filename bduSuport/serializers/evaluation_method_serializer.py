from rest_framework.serializers import ModelSerializer
from ..models.evaluation_method import EvaluationMethod

class EvaluationMethodSerializer(ModelSerializer):
    class Meta: 
        model = EvaluationMethod
        fields = "__all__"