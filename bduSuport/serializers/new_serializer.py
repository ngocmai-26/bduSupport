from rest_framework.serializers import ModelSerializer
from ..models.news_model import New

class NewSerializer(ModelSerializer):
    class Meta: 
        model = New
        fields = ['id', 'title', 'link', 'type', 'image']
        
        