import datetime
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from bduSuport.helpers.paginator import CustomPageNumberPagination
from bduSuport.models.news import News
from bduSuport.helpers.response import RestResponse
from bduSuport.models.news_type import NewsType
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.serializers.news_type_serializer import NewsTypeSerializer

class NewsTypeManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(request_body=NewsTypeSerializer(fields=["name"]))
    def create(self, request):
        try:
            logging.getLogger().info("NewsTypeManagementView.create req=%s", request.data)
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
            logging.getLogger().exception("NewsTypeManagementView.create exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter("size", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ])
    def list(self, request):
        try:
            queryset = NewsType.objects.filter(deleted_at=None).order_by("created_at")
            paginator = CustomPageNumberPagination()
            queryset = paginator.paginate_queryset(queryset, request)
            data = NewsTypeSerializer(queryset, many=True).data

            return RestResponse(data=paginator.get_paginated_data(data), status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("NewsTypeManagementView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    @swagger_auto_schema(request_body=NewsTypeSerializer(fields=["name"]))
    def update(self, request, pk):
        try:
            logging.getLogger().info("NewsTypeManagementView.update pk=%s, req=%s", pk, request.data)
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
            logging.getLogger().exception("NewsManagementView.update exc=%s, pk=%s, req=%s", e, pk, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            logging.getLogger().info("NewsManagementView.destroy pk=%s", pk)
            try:
                news_type = NewsType.objects.get(id=pk)
                news_type.deleted_at = datetime.datetime.now()
                news_type.save(update_fields=["deleted_at"])
                
                return RestResponse(status=status.HTTP_200_OK).response 
            except NewsType.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            logging.getLogger().exception("NewsTypeManagementView.destroy exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response