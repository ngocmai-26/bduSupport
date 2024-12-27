import datetime
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
import logging

from bduSuport.helpers.audit import audit_back_office
from bduSuport.helpers.firebase_storage_provider import FirebaseStorageProvider
from bduSuport.models.news import News
from bduSuport.helpers.response import RestResponse
from bduSuport.serializers.new_serializer import NewsSerializer
from bduSuport.validations.create_news import CreateNewsValidator
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.validations.update_news import UpdateNewsValidator

class NewsManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )
    parser_classes = (MultiPartParser,)
    image_storage_provider = FirebaseStorageProvider()

    @swagger_auto_schema(request_body=CreateNewsValidator)
    def create(self, request):
        try:
            logging.getLogger().info("NewsManagementView.create req=%s", request.data)
            validate = CreateNewsValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            _data = validate.validated_data
            image_url = ""
            
            if _data.get("image", None):
                image_url = self.image_storage_provider.upload_file(_data.pop("image"))
            
            news = News(**_data, author=request.user, deleted_at=None, image=image_url)
            news.save()

            if news.id is None:
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Đã xảy ra lỗi trong quá trình tạo tin tức!").response
            audit_back_office(request.user, "Tạo tin tức", news.title)
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("NewsManagementView.create exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def list(self, request):
        try:
            news = News.objects.filter(deleted_at=None).order_by("created_at")
            data = NewsSerializer(news, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("NewsManagementView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    @swagger_auto_schema(request_body=UpdateNewsValidator)
    def update(self, request, pk):
        try:
            logging.getLogger().info("NewsManagementView.update req=%s", request.data)
            validate = UpdateNewsValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            try:
                news = News.objects.get(id=pk)
            except News.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
            
            _data = validate.validated_data

            if "image" in _data:
                _data["image"] = self.image_storage_provider.upload_file(_data.pop("image"))
            
            for k, v in _data.items():
                setattr(news, k, v)
            
            news.save(update_fields=list(_data.keys()))
            audit_back_office(request.user, "Cập nhật tin tức", news.title)

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("NewsManagementView.update exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            logging.getLogger().info("NewsManagementView.destroy pk=%s", pk)
            try:
                news = News.objects.get(id=pk)
                news.deleted_at = datetime.datetime.now()
                news.save(update_fields=["deleted_at"])
                audit_back_office(request.user, "Xóa tin tức", news.title)
                return RestResponse(status=status.HTTP_200_OK).response 
            except News.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            logging.getLogger().exception("NewsManagementView.destroy exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response