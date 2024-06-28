from rest_framework.serializers import ModelSerializer
from ..models.result_model import Result

class ResultSerializer(ModelSerializer):
    class Meta: 
        model = Result
        fields = ['id', 'subject', 'score', 'password']
        
    