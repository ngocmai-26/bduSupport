import logging
import datetime
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema

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

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("HandbookManagementView.create exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def list(self, request):
        try:
            handbook = Handbook.objects.filter(deleted_at=None).order_by("created_at")
            data = HandbookSerializer(handbook, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response
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
                
                return RestResponse(status=status.HTTP_200_OK).response 
            except Handbook.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            logging.getLogger().exception("HandbookManagementView.destroy exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response