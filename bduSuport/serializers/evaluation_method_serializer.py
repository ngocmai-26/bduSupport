from rest_framework.serializers import ModelSerializer
from ..models.evaluation_method_model import EvaluationMethod

class EvaluationMethodSerializer(ModelSerializer):
    class Meta: 
        model = EvaluationMethod
        fields = ['id', 'name']