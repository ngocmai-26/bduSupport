from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser

from bduSuport.helpers.firebase_storage_provider import FirebaseStorageProvider
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.business_recruitment import BusinessRecruitment
from bduSuport.serializers.business_recruiment import BusinessRecruitmentSerializer
from bduSuport.validations.create_business_recruiment import CreateBusinessRecruimentValidator

class BusinessRecruimentManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )
    parser_classes = (MultiPartParser,)
    image_storage_provider = FirebaseStorageProvider()

    @swagger_auto_schema(request_body=CreateBusinessRecruimentValidator)
    def create(self, request):
        try:
            validate = CreateBusinessRecruimentValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            _data = validate.validated_data
            banner_url = self.image_storage_provider.upload_image(_data.pop("banner"))
            recruiment = BusinessRecruitment(**_data, banner=banner_url, creator=request.user)
            recruiment.save()

            if recruiment.id == None:
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Đã xảy ra lỗi trong quá trình tạo tin tuyển dụng!").response

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"BusinessRecruimentManagementView.create exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def list(self, request):
        try:
            recruiments = BusinessRecruitment.objects.filter(deleted_at=None).order_by("-created_at")
            data = BusinessRecruitmentSerializer(recruiments, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"BusinessRecruimentManagementView.list exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response