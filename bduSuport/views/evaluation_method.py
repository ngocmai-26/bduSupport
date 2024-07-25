from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.evaluation_method import EvaluationMethod
from bduSuport.serializers.evaluation_method_serializer import EvaluationMethodSerializer

class EvaluationMethodView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )
    
    def list(self, request):
        try:
            methods = EvaluationMethod.objects.filter(deleted_at=None)
            data = EvaluationMethodSerializer(methods, many=True).data
            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"SubjectView.list exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response