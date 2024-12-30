import logging
import datetime
from drf_yasg import openapi
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.audit import audit_back_office
from bduSuport.helpers.paginator import CustomPageNumberPagination
from bduSuport.models.handbook import Handbook
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.serializers.handbook import HandbookSerializer
from bduSuport.validations.create_handbook import CreateHandbookValidator
from bduSuport.validations.update_handbook import UpdateHandbookValidator

class HandbookManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(request_body=CreateHandbookValidator)
    def create(self, request):
        try:
            logging.getLogger().info("HandbookManagementView.create req=%s", request.data)
            validate = CreateHandbookValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            handbook = Handbook(**validate.validated_data)
            handbook.save()

            if handbook.id is None:
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Đã xảy ra lỗi trong quá trình tạo tin tức!").response
            audit_back_office(request.user, "Tạo sổ tay", handbook.name)
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("HandbookManagementView.create exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter("size", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ])
    def list(self, request):
        try:
            queryset = Handbook.objects.filter(deleted_at=None).order_by("created_at")
            paginator = CustomPageNumberPagination()
            queryset = paginator.paginate_queryset(queryset, request)
            data = HandbookSerializer(queryset, many=True).data

            return RestResponse(data=paginator.get_paginated_data(data), status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("HandbookManagementView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    @swagger_auto_schema(request_body=UpdateHandbookValidator)
    def partial_update(self, request, pk):
        try:
            logging.getLogger().info("HandbookManagementView.update req=%s", request.data)
            validate = UpdateHandbookValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            try:
                handbook = Handbook.objects.get(id=pk)
            except Handbook.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
            
            for k, v in validate.validated_data.items():
                setattr(handbook, k, v)
            
            handbook.save(update_fields=list(validate.validated_data.keys()))
            audit_back_office(request.user, "Cập nhật sổ tay", handbook.name)
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("HandbookManagementView.update exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            logging.getLogger().info("HandbookManagementView.destroy pk=%s", pk)
            try:
                handbook = Handbook.objects.get(id=pk)
                handbook.deleted_at = datetime.datetime.now()
                handbook.save(update_fields=["deleted_at"])
                audit_back_office(request.user, "Xóa sổ tay", handbook.name)
                return RestResponse(status=status.HTTP_200_OK).response 
            except Handbook.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            logging.getLogger().exception("HandbookManagementView.destroy exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response