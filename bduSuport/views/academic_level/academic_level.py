import datetime
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
import logging

from bduSuport.helpers.response import RestResponse
from bduSuport.models.academic_level import AcademicLevel
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.serializers.academic_level import AcademicLevelSerializer

class AcademicLevelView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(request_body=AcademicLevelSerializer(exclude=["deleted_at"]))
    def create(self, request):
        try:
            logging.getLogger().info("AcademicLevelView.create req=%s", request.data)
            validate = AcademicLevelSerializer(data=request.data, exclude=["deleted_at"])

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            subject = AcademicLevel(name=validate.validated_data["name"])
            subject.save()

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("AcademicLevelView.create exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def list(self, request):
        try:
            subjects = AcademicLevel.objects.filter(deleted_at=None)
            data = AcademicLevelSerializer(subjects, many=True).data
            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("AcademicLevelView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            logging.getLogger().info("AcademicLevelView.destroy pk=%s", pk)
            try:
                level = AcademicLevel.objects.get(id=pk)
                level.deleted_at = datetime.datetime.now().date()
                level.save(update_fields=["deleted_at"])
            except AcademicLevel.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response
            
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("AcademicLevelView.destroy exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response