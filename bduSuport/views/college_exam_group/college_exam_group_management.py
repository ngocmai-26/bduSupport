from datetime import datetime
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction
import logging
from drf_yasg import openapi

from bduSuport.helpers.audit import audit_back_office
from bduSuport.helpers.paginator import CustomPageNumberPagination
from bduSuport.helpers.response import RestResponse
from bduSuport.models.college_exam_group import CollegeExamGroup
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.serializers.college_exam_group import CollegeExamGroupSerializer
from bduSuport.validations.create_college_exam_group import CreateCollegeExamGroupValidator

class CollegeExamGroupView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(request_body=CreateCollegeExamGroupValidator)
    def create(self, request):
        try:
            logging.getLogger().info("CollegeExamGroupView.create req=%s", request.data)
            validate = CreateCollegeExamGroupValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            with transaction.atomic():
                _data = validate.validated_data
                subjects = _data.pop("subjects")
                group = CollegeExamGroup(**_data)
                group.save()
                group.subjects.set(subjects)
                audit_back_office(request.user, "Tạo khối ngành", group.name)

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("CollegeExamGroupView.create exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter("size", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ])
    def list(self, request):
        try:
            queryset = CollegeExamGroup.objects.filter(deleted_at=None).order_by("-created_at")
            paginator = CustomPageNumberPagination()
            queryset = paginator.paginate_queryset(queryset, request)
            data = CollegeExamGroupSerializer(queryset, many=True).data
            return RestResponse(data=paginator.get_paginated_data(data), status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("CollegeExamGroupView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            logging.getLogger().info("CollegeExamGroupView.destroy pk=%s", pk)
            try:
                group = CollegeExamGroup.objects.get(id=pk, deleted_at=None)
                majors = group.majors.filter(deleted_at=None)

                if majors.exists():
                    majors_name = ", ".join([f"'{major.name} ({major.code})'" for major in majors])
                    message = f"Không thể xóa khối ngành vì các ngành {majors_name} đang tham chiếu đến khối ngành này."
                    return RestResponse(status=status.HTTP_400_BAD_REQUEST, message=message).response
                
                group.deleted_at = datetime.now()
                group.save(update_fields=["deleted_at"])
                audit_back_office(request.user, "Xóa khối ngành", group.name)
                
                return RestResponse(status=status.HTTP_200_OK).response
            except CollegeExamGroup.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            logging.getLogger().exception("CollegeExamGroupView.destroy exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response