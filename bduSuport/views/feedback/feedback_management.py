from rest_framework import viewsets, status

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.feedback import Feedback
from bduSuport.serializers.feedback import FeedbackSerializer

class FeedbackManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )
        
    def list(self, request):
        try:
            feedbacks = Feedback.objects.filter(deleted_at=None).order_by("-created_at")
            data = FeedbackSerializer(feedbacks, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"FeedbackManagementView.list exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response