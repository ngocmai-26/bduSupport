from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status

from bduSuport.models.news import News
from bduSuport.helpers.response import RestResponse
from bduSuport.serializers.new_serializer import NewsSerializer
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication

class MiniappNewsView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )

    @swagger_auto_schema(manual_parameters=[openapi.Parameter("type", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)])
    def list(self, request):
        try:
            news_type_filter = None
            
            if request.query_params.get("type", "").isdigit():
                news_type_filter = int(request.query_params["type"])
            
            news = News.objects.filter(deleted_at=None).order_by("created_at")

            if news_type_filter is not None: 
                news = news.filter(type__id=news_type_filter)

            data = NewsSerializer(news, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"MiniappNewsView.list exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response