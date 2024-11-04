from rest_framework import viewsets, status
import logging

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.models.training_location import TrainingLocation
from bduSuport.serializers.training_location import TrainingLocationSerializer

class MiniappTrainingLocationView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )

    def list(self, request):
        try:
            subjects = TrainingLocation.objects.filter(deleted_at=None)
            data = TrainingLocationSerializer(subjects, many=True).data
            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("MiniappTrainingLocationView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response