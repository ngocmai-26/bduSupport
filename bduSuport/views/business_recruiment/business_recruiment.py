from rest_framework import viewsets, status
import logging

from bduSuport.helpers.response import RestResponse
from bduSuport.models.business_recruitment import BusinessRecruitment
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.serializers.business_recruiment import BusinessRecruitmentSerializer

class BusinessRecruimentView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )
        
    def list(self, request):
        try:
            recruiments = BusinessRecruitment.objects.filter(deleted_at=None).order_by("-created_at")
            data = BusinessRecruitmentSerializer(recruiments, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("BusinessRecruimentView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response