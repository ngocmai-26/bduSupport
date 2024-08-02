import datetime
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema

from bduSuport.models.news import News
from bduSuport.helpers.response import RestResponse
from bduSuport.models.news_type import NewsType
from bduSuport.serializers.new_serializer import NewsSerializer
from bduSuport.validations.create_news import CreateNewsValidator
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.validations.update_news import UpdateNewsValidator
from bduSuport.serializers.news_type_serializer import NewsTypeSerializer

class NewsTypeManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(request_body=NewsTypeSerializer(fields=["name"]))
    def create(self, request):
        try:
            validate = NewsTypeSerializer(data=request.data, fields=["name"])

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            _data = validate.validated_data
            
            news_type = NewsType(**_data, author=request.user, deleted_at=None)
            news_type.save()

            if news_type.id is None:
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Đã xảy ra lỗi trong quá trình tạo loại tin tức!").response

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"NewsTypeManagementView.create exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def list(self, request):
        try:
            news_types = NewsType.objects.filter(deleted_at=None).order_by("created_at")
            data = NewsTypeSerializer(news_types, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"NewsTypeManagementView.list exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    @swagger_auto_schema(request_body=NewsTypeSerializer(fields=["name"]))
    def update(self, request, pk):
        try:
            validate = NewsTypeSerializer(data=request.data, fields=["name"])

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            try:
                news_type = NewsType.objects.get(id=pk, deleted_at=None)
            except NewsType.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
            
            _data = validate.validated_data
            
            for k, v in _data.items():
                setattr(news_type, k, v)
            
            news_type.save(update_fields=list(_data.keys()))

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"NewsManagementView.update exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            try:
                news_type = NewsType.objects.get(id=pk)
                news_type.deleted_at = datetime.datetime.now()
                news_type.save(update_fields=["deleted_at"])
                
                return RestResponse(status=status.HTTP_200_OK).response 
            except NewsType.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            print(f"NewsTypeManagementView.detroy exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response