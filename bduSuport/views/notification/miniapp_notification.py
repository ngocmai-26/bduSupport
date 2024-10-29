import logging
from rest_framework.viewsets import ViewSet
from rest_framework import status

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.models.miniapp_notification import MiniappNotification
from bduSuport.serializers.miniapp_notification import MiniappNotificationSerializer

class MiniappNotificationView(ViewSet):
    authentication_classes = (MiniAppAuthentication, )

    def list(self, request):
        try:
            noti = MiniappNotification.objects.filter(deleted_at=None, user=request.user).order_by("created_at")
            data = MiniappNotificationSerializer(noti, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("MiniappNewsView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response