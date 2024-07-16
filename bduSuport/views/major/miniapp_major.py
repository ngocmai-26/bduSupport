from rest_framework import viewsets, status
from rest_framework.decorators import action

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.models.evaluation_method import EvaluationMethod
from bduSuport.serializers.evaluation_method_serializer import EvaluationMethodSerializer

class MiniappMajorView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )

    @action(methods=["GET"], detail=True, url_path="evaluation-methods")
    def get_evaluation_methods_by_acadmic_major(self, request, pk):
        try:
            methods = EvaluationMethod.objects.filter(majors__id=pk)
            data = EvaluationMethodSerializer(methods, many=True).data
            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"MiniappMajorView.get_evaluation_methods_by_acadmic_major exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response