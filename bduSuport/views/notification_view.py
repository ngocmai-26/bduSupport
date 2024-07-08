from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.notification_model import Notification
from ..serializers.notification_serializer import NotificationSerializer, NotificationIsActiveSerializer


class NotificationView(viewsets.ViewSet):
    def list(self, request):
        queryset = Notification.objects.all()
        serializer = NotificationSerializer(queryset, many=True)
        return Response({
            "message": "Notifications retrieved successfully.",
            "data": serializer.data
        })

    def create(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Notification created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Failed to create notification.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            notification = Notification.objects.get(pk=pk)
            serializer = NotificationSerializer(notification)
            return Response({
                "message": "Notification retrieved successfully.",
                "data": serializer.data
            })
        except Notification.DoesNotExist:
            return Response({
                "message": "Notification not found."
            }, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        # Chỉ cập nhật trường 'is_active'
        try:
            notification = Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            return Response({
                "message": "Notification not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = NotificationIsActiveSerializer(notification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Notification is_active updated successfully.",
                "data": serializer.data
            })
        return Response({
            "message": "Failed to update notification.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            notification = Notification.objects.get(pk=pk)
            notification.delete()
            return Response({
                "message": "Notification deleted successfully."
            }, status=status.HTTP_204_NO_CONTENT)
        except Notification.DoesNotExist:
            return Response({
                "message": "Notification not found."
            }, status=status.HTTP_404_NOT_FOUND)
    

