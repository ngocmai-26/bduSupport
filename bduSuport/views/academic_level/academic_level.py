import datetime
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
import logging
from drf_yasg import openapi

from bduSuport.helpers.audit import audit_back_office
from bduSuport.helpers.paginator import CustomPageNumberPagination
from bduSuport.helpers.response import RestResponse
from bduSuport.models.academic_level import AcademicLevel
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.serializers.academic_level import AcademicLevelSerializer
from bduSuport.validations.update_academic_level import UpdateAcademicLevelValidator

class AcademicLevelView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(request_body=AcademicLevelSerializer(exclude=["deleted_at"]))
    def create(self, request):
        try:
            logging.getLogger().info("AcademicLevelView.create req=%s", request.data)
            validate = AcademicLevelSerializer(data=request.data, exclude=["deleted_at"])

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            academic_level = AcademicLevel(
                name=validate.validated_data["name"],
                need_evaluation_method=validate.validated_data["need_evaluation_method"]
            )
            academic_level.save()
            audit_back_office(request.user, "Tạo bậc học", academic_level.name)
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("AcademicLevelView.create exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter("size", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ])
    def list(self, request):
        try:
            queryset = AcademicLevel.objects.filter(deleted_at=None)
            paginator = CustomPageNumberPagination()
            queryset = paginator.paginate_queryset(queryset, request)
            data = AcademicLevelSerializer(queryset, many=True).data
            return RestResponse(data=paginator.get_paginated_data(data), status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("AcademicLevelView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    @swagger_auto_schema(request_body=UpdateAcademicLevelValidator)
    def update(self, request, pk):
        try:
            validate = UpdateAcademicLevelValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            _data = validate.validated_data

            if "need_evaluation_method" not in request.data:
                _data.pop("need_evaluation_method")

            level = AcademicLevel.objects.get(id=pk)
            old_name = level.name
            old_need_evaluation_method = level.need_evaluation_method

            for k, v in _data.items():
                setattr(level, k, v)

            level.save()
            audit_back_office(
                request.user, 
                "Cập nhật bậc học", 
                f"Tên: {old_name} -> {level.name}\nXét tuyển: {old_need_evaluation_method} -> {level.need_evaluation_method}"
            )
            return RestResponse(status=status.HTTP_200_OK).response
        except AcademicLevel.DoesNotExist as e:
            return RestResponse(status=status.HTTP_404_NOT_FOUND).response
        except Exception as e:
            logging.getLogger().exception("AcademicLevelView.update exc=%s, pk=%s, req=%s", e, pk, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            logging.getLogger().info("AcademicLevelView.destroy pk=%s", pk)
            try:
                level = AcademicLevel.objects.get(id=pk)
                majors = level.majors.filter(deleted_at=None)

                if majors.exists():
                    codes = ", ".join([f"'{major.code}'" for major in majors])
                    message = f"Không thể xóa trình độ đào tạo vì các ngành {codes} đang tham chiếu đến trình độ đào tạo này."
                    return RestResponse(status=status.HTTP_400_BAD_REQUEST, message=message).response
                
                level.deleted_at = datetime.datetime.now().date()
                level.save(update_fields=["deleted_at"])
                audit_back_office(request.user, "Xóa bậc học", level.name)
            except AcademicLevel.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response
            
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("AcademicLevelView.destroy exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response