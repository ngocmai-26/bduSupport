from rest_framework.serializers import ModelSerializer
from ..models.major_model import Major

class MajorSerializer(ModelSerializer):
    class Meta: 
        model = Major
        fields = ['id', 'name', 'industryCode', 'targets', 'combination', 'description', 'year', 'benchmark', 'tuition', 'trainingLocation']
       
    