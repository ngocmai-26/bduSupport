from django.http import HttpResponse
from rest_framework import viewsets, permissions
from ..models.notification_model import Notification
from ..serializers.notification_serializer import NotificationSerializer
# Create your views here.

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    

def index(request):
    return HttpResponse("Hello My App")