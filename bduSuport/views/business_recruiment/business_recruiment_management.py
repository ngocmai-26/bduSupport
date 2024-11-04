import datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
import logging

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
            logging.getLogger().info("BusinessRecruimentManagementView.create req=%s", request.data)
            validate = CreateBusinessRecruimentValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            _data = validate.validated_data
            banner_url = self.image_storage_provider.upload_file(_data.pop("banner"))
            recruiment = BusinessRecruitment(**_data, banner=banner_url, creator=request.user)
            recruiment.save()

            if recruiment.id == None:
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Đã xảy ra lỗi trong quá trình tạo tin tuyển dụng!").response

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("BusinessRecruimentManagementView.create exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def list(self, request):
        try:
            recruiments = BusinessRecruitment.objects.filter(deleted_at=None).order_by("-created_at")
            data = BusinessRecruitmentSerializer(recruiments, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("BusinessRecruimentManagementView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            logging.getLogger().info("BusinessRecruimentManagementView.create pk=%s", pk)
            try:
                recruiment = BusinessRecruitment.objects.get(id=pk)
                recruiment.deleted_at = datetime.datetime.now().date()
                recruiment.save(update_fields=["deleted_at"])
            except BusinessRecruitment.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response
            
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("BusinessRecruimentManagementView.list exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response