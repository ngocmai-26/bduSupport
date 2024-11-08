import datetime
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
import logging

from bduSuport.helpers.response import RestResponse
from bduSuport.models.academic_level import AcademicLevel
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.serializers.academic_level import AcademicLevelSerializer
from bduSuport.validations.update_academic_level import UpdateAcademicLevelValidator

class AcademicLevelView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(request_body=AcademicLevelSerializer(exclude=["deleted_at"]))
    def create(self, request):
        try:
            logging.getLogger().info("AcademicLevelView.create req=%s", request.data)
            validate = AcademicLevelSerializer(data=request.data, exclude=["deleted_at"])

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            subject = AcademicLevel(
                name=validate.validated_data["name"],
                need_evaluation_method=validate.validated_data["need_evaluation_method"]
            )
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
        
    @swagger_auto_schema(request_body=UpdateAcademicLevelValidator)
    def update(self, request, pk):
        try:
            validate = UpdateAcademicLevelValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            level = AcademicLevel.objects.get(id=pk)

            for k, v in validate.validated_data.items():
                setattr(level, k, v)

            level.save()
            return RestResponse(status=status.HTTP_200_OK).response
        except AcademicLevel.DoesNotExist as e:
            return RestResponse(status=status.HTTP_404_NOT_FOUND).response
        except Exception as e:
            logging.getLogger().exception("AcademicLevelView.update exc=%s, pk=%s, req=%s", e, pk, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            logging.getLogger().info("AcademicLevelView.destroy pk=%s", pk)
            try:
                level = AcademicLevel.objects.get(id=pk)
                majors = level.majors.filter(deleted_at=None)

                if majors.exists():
                    codes = ", ".join([f"'{major.code}'" for major in majors])
                    message = f"Không thể xóa trình độ đào tạo vì các ngành {codes} đang tham chiếu đến trình độ đào tạo này."
                    return RestResponse(status=status.HTTP_400_BAD_REQUEST, message=message).response
                
                level.deleted_at = datetime.datetime.now().date()
                level.save(update_fields=["deleted_at"])
            except AcademicLevel.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response
            
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("AcademicLevelView.destroy exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response