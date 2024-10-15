from rest_framework import viewsets, status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
import logging

from bduSuport.helpers.response import RestResponse
from bduSuport.models.academic_level import AcademicLevel
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.models.major import Major
from bduSuport.serializers.academic_level import AcademicLevelSerializer
from bduSuport.serializers.major_serializer import MajorSerializer

class MiniappAcademicLevelView(viewsets.ViewSet):
    # authentication_classes = (MiniAppAuthentication, )

    @action(methods=["GET"], detail=True, url_path="majors")
    def get_majors_by_acadmic_level(self, request, pk):
        try:
            logging.getLogger().info("AcademicLevelView.get_majors_by_acadmic_level pk=%s", pk)
            majors = Major.objects.filter(academic_level__id=pk)
            data = MajorSerializer(majors, many=True).data
            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("AcademicLevelView.get_majors_by_acadmic_level exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response