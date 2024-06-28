from rest_framework.serializers import ModelSerializer
from ..models.notification_model import Notification

class NotificationSerializer(ModelSerializer):
    class Meta: 
        model = Notification
        fields = ['id', 'title', 'content', 'trainingLocation', 'tuition', 'benchmark', 'year', 'image', 'account']
        