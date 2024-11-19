import logging
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from bduSuport.helpers.firebase_storage_provider import FirebaseStorageProvider
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.validations.create_media import CreateMediaValidator
from bduSuport.validations.delete_media import DeleteMediaValidator

class MediaView(viewsets.ViewSet):
    # authentication_classes = (MiniAppAuthentication, )
    parser_classes = (MultiPartParser,)
    file_storage_provider = FirebaseStorageProvider()

    @swagger_auto_schema(request_body=CreateMediaValidator)
    def create(self, request):
        try:
            logging.getLogger().info("MediaView.create req=%s", request.data)
            validate = CreateMediaValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            
            file_url = self.file_storage_provider.upload_file(request.data["file"])
            
            # return RestResponse(data=file_url, status=status.HTTP_200_OK).response
            return Response(
                data={
                    "error": 0,
                    "code": status.HTTP_200_OK,
                    "message": "Thành công!",
                    "data": file_url
                },
                status=status.HTTP_200_OK,
                content_type = "application/json"
            )
        except Exception as e:
            logging.getLogger().exception("MediaView.create exc=%s", e)
            # return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
            return Response(
                data={
                    "error": 1,
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "Thành công!",
                    "data": None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type = "application/json"
            )
        
    @action(methods=["DELETE"], detail=False, url_path="remove")
    @swagger_auto_schema(request_body=DeleteMediaValidator)
    def delete_file(self, request):
        try:
            logging.getLogger().info("MediaView.delete_file req=%s", request.data)
            validate = DeleteMediaValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            self.file_storage_provider.delete_file(request.data["url"])

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("MediaView.delete_file exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response