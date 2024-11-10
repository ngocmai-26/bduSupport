from rest_framework import serializers
from ..models.miniapp_notification import MiniappNotification

class MiniappNotificationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = MiniappNotification
        fields = "__all__"

    is_read = serializers.SerializerMethodField()

    def get_is_read(self, obj: MiniappNotification):
        return obj.read_at is not None
        
        