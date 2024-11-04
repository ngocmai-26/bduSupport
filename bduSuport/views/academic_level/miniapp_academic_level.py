import logging
from drf_yasg import openapi
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.response import RestResponse
from bduSuport.models.academic_level import AcademicLevel
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.models.major import Major
from bduSuport.serializers.major_serializer import MajorSerializer
from bduSuport.validations.training_location_filter import TrainingLocationFilter

class MiniappAcademicLevelView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )

    @action(methods=["GET"], detail=True, url_path="majors")
    @swagger_auto_schema(manual_parameters=[openapi.Parameter("training_location", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)])
    def get_majors_by_academic_level(self, request, pk):
        try:
            logging.getLogger().info("AcademicLevelView.get_majors_by_academic_level pk=%s, query_params=%s", pk, request.query_params)
            validate = TrainingLocationFilter(data=request.query_params)

            if not validate.is_valid():
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response

            query = Q(academic_level__id=pk)
            location = validate.validated_data.get("training_location", None)

            if location is not None:
                query = query & Q(training_location=location)
                
            majors = Major.objects.filter(query)
            data = MajorSerializer(majors, many=True).data
            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("AcademicLevelView.get_majors_by_academic_level exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response