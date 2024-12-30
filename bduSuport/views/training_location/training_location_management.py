import datetime
import logging
from rest_framework import viewsets, status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.audit import audit_back_office
from bduSuport.helpers.paginator import CustomPageNumberPagination
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.training_location import TrainingLocation
from bduSuport.serializers.training_location import TrainingLocationSerializer

class TrainingLocationView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(request_body=TrainingLocationSerializer(exclude=["deleted_at"]))
    def create(self, request):
        try:
            logging.getLogger().info("TrainingLocationView.create req=%s", request.data)
            validate = TrainingLocationSerializer(data=request.data, exclude=["deleted_at"])

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            location = TrainingLocation(
                name=validate.validated_data["name"],
            )
            location.save()
            audit_back_office(request.user, "Tạo địa điểm giảng dạy", location.name)
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("TrainingLocationView.create exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter("size", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ])
    def list(self, request):
        try:
            queryset = TrainingLocation.objects.filter(deleted_at=None).order_by("-created_at")
            paginator = CustomPageNumberPagination()
            queryset = paginator.paginate_queryset(queryset, request)
            data = TrainingLocationSerializer(queryset, many=True).data
            return RestResponse(data=paginator.get_paginated_data(data), status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("TrainingLocationView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            logging.getLogger().info("TrainingLocationView.destroy pk=%s", pk)
            try:
                location = TrainingLocation.objects.get(id=pk)
                majors = location.majors.filter(deleted_at=None)

                if majors.exists():
                    majors_name = ", ".join([f"'{major.name} ({major.code})'" for major in majors])
                    message = f"Không thể xóa nơi đào tạo vì các ngành {majors_name} đang tham chiếu đến nơi đào tạo này."
                    return RestResponse(status=status.HTTP_400_BAD_REQUEST, message=message).response
                
                location.deleted_at = datetime.datetime.now().date()
                location.save(update_fields=["deleted_at"])
                audit_back_office(request.user, "Xóa địa điểm giảng dạy", location.name)
            except TrainingLocation.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response
            
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("TrainingLocationView.destroy exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response