import logging
from rest_framework import viewsets, status

from bduSuport.models.handbook import Handbook
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.serializers.handbook import HandbookSerializer

class HandbookView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )

    def list(self, request):
        try:
            handbook = Handbook.objects.filter(deleted_at=None).order_by("created_at")
            data = HandbookSerializer(handbook, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("HandbookMiniappView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response