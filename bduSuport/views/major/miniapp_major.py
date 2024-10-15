from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import logging

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.models.evaluation_method import EvaluationMethod
from bduSuport.models.major import Major
from bduSuport.serializers.college_exam_group import CollegeExamGroupSerializer
from bduSuport.serializers.evaluation_method_serializer import EvaluationMethodSerializer
from bduSuport.serializers.major_serializer import MajorSerializer
from bduSuport.validations.majors_filter import MajorsFilter

class MiniappMajorView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("year", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter("academic_level", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    ])
    def list(self, request):
        try:
            logging.getLogger().info("MiniappMajorView.list query_params=%s", request.query_params)
            validate = MajorsFilter(data=request.query_params)

            if not validate.is_valid():
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            _data = validate.validated_data
            majors = Major.objects.filter(Q(**_data))
            data = MajorSerializer(majors, many=True).data
            
            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("MiniappMajorView.list exc=%s, query_params=%s", e, request.query_params)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response

    @action(methods=["GET"], detail=True, url_path="evaluation-methods")
    def get_evaluation_methods_by_academic_major(self, request, pk):
        try:
            logging.getLogger().info("MiniappMajorView.get_evaluation_methods_by_academic_major pk=%s", pk)
            methods = EvaluationMethod.objects.filter(majors__id=pk)
            data = EvaluationMethodSerializer(methods, many=True).data
            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("MiniappMajorView.get_evaluation_methods_by_academic_major exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    @action(methods=["GET"], detail=True, url_path="college-exam-groups")
    def get_college_exam_groups_by_academic_major(self, request, pk):
        try:
            try:
                logging.getLogger().info("MiniappMajorView.get_college_exam_groups_by_academic_major pk=%s", pk)
                groups = Major.objects.get(id=pk).college_exam_groups.all()
                data = CollegeExamGroupSerializer(groups, many=True).data
                return RestResponse(data=data, status=status.HTTP_200_OK).response
            except Major.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response
        except Exception as e:
            logging.getLogger().exception("MiniappMajorView.get_college_exam_groups_by_academic_major exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response