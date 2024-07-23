from rest_framework import viewsets, status

from bduSuport.models.news import News
from bduSuport.helpers.response import RestResponse
from bduSuport.serializers.new_serializer import NewsSerializer
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication

class MiniappNewsView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )

    def list(self, request):
        try:
            news = News.objects.filter(deleted_at=None).order_by("created_at")
            data = NewsSerializer(news, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"MiniappNewsView.list exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response