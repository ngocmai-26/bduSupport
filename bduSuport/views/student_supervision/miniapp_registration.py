import datetime
import logging
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from bduSuport.helpers.paginator import CustomPageNumberPagination
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.models.student_supervision_registration import StudentSupervisionRegistration
from bduSuport.validations.submit_student_supervision_registration import SubmitStudentSupervisionRegistration
from bduSuport.services.bdu_dw.bdu_dw import BduDwService
from bduSuport.serializers.student_supervision_registration import StudentSupervisionRegistrationSerializer

class MiniappStudentSupervisionRegistrationView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )

    @swagger_auto_schema(request_body=SubmitStudentSupervisionRegistration)
    def create(self, request):
        try:
            logging.getLogger().info("MiniappStudentSupervisionRegistrationView.create req=%s", request.data)
            validate = SubmitStudentSupervisionRegistration(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            student_code = validate.validated_data["student_code"]
            citizen_id = validate.validated_data["citizen_id"]
            birthday = validate.validated_data["birthday"]

            student = BduDwService().get_student(student_code)

            if student is None:
                return RestResponse(data=None, status=status.HTTP_400_BAD_REQUEST, message="Mã số sinh viên không tồn tại!").response
            
            if student.id_card != citizen_id or birthday != student.date_of_birth:
                return RestResponse(data=None, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại thông tin sinh viên!").response
            
            if StudentSupervisionRegistration.objects.filter(
                student_dw_code=student_code,
                miniapp_user=request.user,
                deleted_at=None
            ).exists():
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message=f"Bạn đã đăng ký nhận thông tin về sinh viên này trước đây!").response

            StudentSupervisionRegistration(
                student_dw_code=student_code,
                student_full_name=student.full_name,
                miniapp_user=request.user
            ).save()

            return RestResponse(status=status.HTTP_200_OK, message=f"Đăng ký nhận thông tin về  sinh viên {student.student_id} - {student.full_name} thành công!").response
        except Exception as e:
            logging.getLogger().exception("MiniappStudentSupervisionRegistrationView.create exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter("size", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ]) 
    def list(self, request):
        try:
            queryset = StudentSupervisionRegistration.objects.filter(miniapp_user=request.user, deleted_at=None).order_by("-created_at")
            paginator = CustomPageNumberPagination()
            queryset = paginator.paginate_queryset(queryset, request)
            data = StudentSupervisionRegistrationSerializer(queryset, many=True).data

            return RestResponse(data=paginator.get_paginated_data(data), status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("MiniappStudentSupervisionRegistrationView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            registration = StudentSupervisionRegistration.objects.get(miniapp_user=request.user, deleted_at=None, id=pk)
            registration.deleted_at = datetime.datetime.now()
            registration.save()

            return RestResponse().response
        except StudentSupervisionRegistration.DoesNotExist:
            return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Bạn chưa đăng ký nhận thông tin của sinh viên này!").response
        except Exception as e:
            logging.getLogger().exception("MiniappStudentSupervisionRegistrationView.destroy exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response