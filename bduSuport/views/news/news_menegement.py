from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.firebase_storage_provider import FirebaseStorageProvider
from bduSuport.models.news import News
from bduSuport.helpers.response import RestResponse
from bduSuport.serializers.new_serializer import NewsSerializer
from bduSuport.validations.create_news import CreateNewsValidator
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication

class NewsManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )
    parser_classes = (MultiPartParser,)
    image_storage_provider = FirebaseStorageProvider()

    @swagger_auto_schema(request_body=CreateNewsValidator)
    def create(self, request):
        try:
            validate = CreateNewsValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST).response
            
            _data = validate.validated_data
            image_url = self.image_storage_provider.upload_image(_data.pop("image"))
            
            news = News(**_data, author=request.user, deleted_at=None, image=image_url)
            news.save()

            if news.id is None:
                return RestResponse(status=status.HTTP_400_BAD_REQUEST).response

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"SubjectView.create exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response