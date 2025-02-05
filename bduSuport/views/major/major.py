from datetime import datetime
from django.db.models import Q
from rest_framework import viewsets, status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction
import logging

from bduSuport.helpers.audit import audit_back_office
from bduSuport.helpers.paginator import CustomPageNumberPagination
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.major import Major
from bduSuport.serializers.major_serializer import MajorSerializer
from bduSuport.validations.create_major import CreateMajorValidator
from bduSuport.validations.majors_filter import MajorsFilter
from bduSuport.validations.update_major import UpdateMajorValidator

class MajorView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )
    
    @swagger_auto_schema(request_body=CreateMajorValidator)
    def create(self, request):
        try:
            logging.getLogger().info("MajorView.create req=%s", request.data)
            validate = CreateMajorValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            with transaction.atomic():
                _data = validate.validated_data
                college_exam_groups = _data.pop("college_exam_groups")
                evaluation_methods = _data.pop("evaluation_methods")
                major = Major(**_data)
                major.save()

                if major.academic_level.need_evaluation_method:
                    major.college_exam_groups.set(college_exam_groups)
                    major.evaluation_methods.set(evaluation_methods)
            audit_back_office(request.user, "Tạo ngành học", major.code)
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("MajorView.create exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter("size", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter("training_location", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    ])
    def list(self, request):
        try:
            validate = MajorsFilter(data=request.query_params, fields=["training_location"])

            if not validate.is_valid():
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            _data = validate.validated_data
            queryset = Major.objects.filter(Q(**_data) & Q(deleted_at=None)).order_by("-created_at")
            paginator = CustomPageNumberPagination()
            queryset = paginator.paginate_queryset(queryset, request)
            data = MajorSerializer(queryset, many=True).data
            return RestResponse(data=paginator.get_paginated_data(data), status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("MajorView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            logging.getLogger().info("MajorView.destroy pk=%s", pk)
            try:
                major = Major.objects.get(id=pk)
                major.deleted_at = datetime.now().date()
                major.save(update_fields=["deleted_at"])
                audit_back_office(request.user, "Xóa ngành học", major.code)
            except Major.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response
            
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("MajorView.destroy exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    @swagger_auto_schema(request_body=UpdateMajorValidator)
    def update(self, request, pk):
        try:
            logging.getLogger().info("MajorView.update pk=%s, req=%s", pk, request.data)
            validate = UpdateMajorValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            with transaction.atomic():
                try:
                    major = Major.objects.get(id=pk, deleted_at=None)
                    _data = validate.validated_data
                    college_exam_groups = _data.pop("college_exam_groups", None)
                    evaluation_methods = _data.pop("evaluation_methods", None)
                    code = _data.get("code", None)
                    year = _data.get("year", None)
                    academic_level = _data.get("academic_level", None)
                    training_location = _data.get("training_location", None)

                    unique_query = Q(deleted_at=None) & ~Q(id=pk)

                    if code is not None:
                        unique_query = unique_query & Q(code=code)
                    else:
                        unique_query = unique_query & Q(code=major.code)

                    if year is not None:
                        unique_query = unique_query & Q(year=year)
                    else:
                        unique_query = unique_query & Q(year=major.year)

                    if academic_level is not None:
                        unique_query = unique_query & Q(academic_level=academic_level)
                    else:
                        unique_query = unique_query & Q(academic_level=major.academic_level)

                    if training_location is not None:
                        unique_query = unique_query & Q(training_location=training_location)
                    else:
                        unique_query = unique_query & Q(training_location=major.training_location)

                    if Major.objects.filter(unique_query).exists():
                        return RestResponse(message="Thông tin ngành hợp không hợp lệ!", status=status.HTTP_400_BAD_REQUEST).response

                    for k, v in _data.items():
                        setattr(major, k, v)

                    major.save()
                    
                    if college_exam_groups is not None:
                        major.college_exam_groups.set(college_exam_groups)

                    if evaluation_methods is not None:
                        major.evaluation_methods.set(evaluation_methods)

                except Major.DoesNotExist:
                    return RestResponse(status=status.HTTP_404_NOT_FOUND).response
            
            audit_back_office(request.user, "Cập nhật ngành học", major.code)
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("MajorView.update exc=%s, pk=%s, req=%s", e, pk, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response