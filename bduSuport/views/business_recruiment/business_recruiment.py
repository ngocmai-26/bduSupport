from rest_framework import viewsets, status

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
            print(f"BusinessRecruimentView.list exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response