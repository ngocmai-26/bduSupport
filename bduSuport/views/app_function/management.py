import datetime
import logging
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.firebase_storage_provider import FirebaseStorageProvider
from bduSuport.helpers.response import RestResponse
from bduSuport.models.app_function import AppFunction
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.middlewares.permissions.is_root import IsRoot
from bduSuport.serializers.app_function import AppFunctionSerializer
from bduSuport.validations.create_app_function import CreateAppFunctionSerializer
from bduSuport.validations.update_app_function import UpdateAppFunctionSerializer

class AppFunctionManagementView(viewsets.ViewSet):
    # authentication_classes = (BackofficeAuthentication, )
    # permission_classes = (IsRoot,)
    parser_classes = (MultiPartParser,)
    image_storage_provider = FirebaseStorageProvider()

    @swagger_auto_schema(request_body=CreateAppFunctionSerializer)
    def create(self, request):
        try:
            logging.getLogger().info("AppFunctionManagementView.create req=%s", request.data)
            validate = CreateAppFunctionSerializer(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            _data = validate.validated_data
            icon_url = self.image_storage_provider.upload_file(_data.pop("icon"))
            app_func = AppFunction(**_data, icon_url=icon_url)
            app_func.save()

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("AppFunctionManagementView.create exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    def list(self, request):
        try:
            funcs = AppFunction.objects.filter(deleted_at=None).order_by("-order")
            data = AppFunctionSerializer(funcs, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("AppFunctionManagementView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            logging.getLogger().info("AppFunctionManagementView.create pk=%s", pk)
            try:
                func = AppFunction.objects.get(id=pk)
                func.deleted_at = datetime.datetime.now().date()
                func.save(update_fields=["deleted_at"])
            except AppFunction.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response
            
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("AppFunctionManagementView.list exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    @swagger_auto_schema(request_body=UpdateAppFunctionSerializer)
    def partial_update(self, request, pk):
        try:
            logging.getLogger().info("AppFunctionManagementView.partial_update req=%s", request.data)
            validate = UpdateAppFunctionSerializer(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            _data = validate.validated_data
            icon = _data.pop("icon", None)

            try:
                func = AppFunction.objects.get(id=pk)
            except AppFunction.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response
            
            for k,v in _data.items():
                setattr(func, k, v)

            if icon:
                icon_url = self.image_storage_provider.upload_file(_data.pop("icon"))
                func.icon_url = icon_url
            
            func.save()

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("AppFunctionManagementView.partial_update exc=%s, pk=%s, req=%s", e, pk, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response