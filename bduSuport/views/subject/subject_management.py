import logging
from datetime import datetime
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from bduSuport.helpers.audit import audit_back_office
from bduSuport.helpers.paginator import CustomPageNumberPagination
from bduSuport.helpers.response import RestResponse
from bduSuport.models.subject import Subject
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.serializers.subject import SubjectSerializer

class SubjectView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(request_body=SubjectSerializer(exclude=["deleted_at"]))
    def create(self, request):
        try:
            logging.getLogger().info("SubjectView.create req=%s", request.data)
            validate = SubjectSerializer(data=request.data, exclude=["deleted_at"])

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            subject = Subject(name=validate.validated_data["name"])
            subject.save()
            audit_back_office(request.user, "Tạo môn học", subject.name)
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("SubjectView.create exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter("size", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ])
    def list(self, request):
        try:
            queryset = Subject.objects.filter(deleted_at=None).order_by("-created_at")
            paginator = CustomPageNumberPagination()
            queryset = paginator.paginate_queryset(queryset, request)
            data = SubjectSerializer(queryset, many=True).data
            return RestResponse(data=paginator.get_paginated_data(data), status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("SubjectView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            logging.getLogger().info("SubjectView.destroy pk=%s", pk)
            try:
                subject = Subject.objects.get(id=pk, deleted_at=None)
                college_groups = subject.college_groups.filter(deleted_at=None)

                if college_groups.exists():
                    gr_name = ", ".join([f"'{group.code}'" for group in college_groups])
                    message = f"Không thể xóa môn học vì các khối ngành {gr_name} đang tham chiếu đến môn học này."
                    return RestResponse(status=status.HTTP_400_BAD_REQUEST, message=message).response
                
                subject.deleted_at = datetime.now()
                subject.save(update_fields=["deleted_at"])
                audit_back_office(request.user, "Xóa môn học", subject.name)
                return RestResponse(status=status.HTTP_200_OK).response
            except Subject.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            logging.getLogger().exception("SubjectView.destroy exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response