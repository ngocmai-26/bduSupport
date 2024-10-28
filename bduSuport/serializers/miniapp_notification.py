from rest_framework.serializers import ModelSerializer
from ..models.miniapp_notification import MiniappNotification

class MiniappNotificationSerializer(ModelSerializer):
    class Meta: 
        model = MiniappNotification
        fields = "__all__"
        
        