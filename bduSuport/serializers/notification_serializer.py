from rest_framework.serializers import ModelSerializer
from ..models.notification_model import Notification

class NotificationSerializer(ModelSerializer):
    class Meta: 
        model = Notification
        fields = ['id', 'title', 'content', 'type', 'is_active',  'image', 'account']
        
class NotificationIsActiveSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ['is_active']
        