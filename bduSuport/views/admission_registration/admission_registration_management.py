from django.db.models import Q
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, status
from rest_framework.decorators import action

from bduSuport.helpers.email import EmailProvider
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.admission_registration import AdmissionRegistration, ReviewStatusChoices
from bduSuport.serializers.admission_registration_serializer import AdmissionRegistrationSerializer
from bduSuport.validations.list_admission_registration_filter import ListAdmissionRegistrationFilter
from bduSuport.validations.review_registration import ReviewRegistrationValidator
from bduSuport.models.miniapp_notification import MiniappNotification
from bduSuport.models.subject import Subject

class AdmissionRegistrationManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )
    email_provider = EmailProvider()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("evaluation_method", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("major", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("college_exam_group", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter("review_status", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=ReviewStatusChoices.values),
        ]
    )
    def list(self, request):
        try:
            logging.getLogger().info("AdmissionRegistrationManagementView.list query_params=%s", request.query_params)
            validate = ListAdmissionRegistrationFilter(data=request.query_params)

            if not validate.is_valid():
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            query_condition = Q(**validate.validated_data, recalled_at=None)
            registrations = AdmissionRegistration.objects.filter(query_condition)
            data = AdmissionRegistrationSerializer(registrations, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response 
        except Exception as e:
            logging.getLogger().exception("AdmissionRegistrationManagementView.list exc=%s, params=%s", e, request.query_params)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response

    def retrieve(self, request, pk):
        try:
            logging.getLogger().info("AdmissionRegistrationManagementView.retrieve pk=%s", pk)
            try:
                registration = AdmissionRegistration.objects.get(id=pk)
                data = AdmissionRegistrationSerializer(registration).data
                return RestResponse(data=data, status=status.HTTP_200_OK).response 
            
            except AdmissionRegistration.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            logging.getLogger().exception("AdmissionRegistrationManagementView.retrieve exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    @swagger_auto_schema(request_body=ReviewRegistrationValidator)
    @action(methods=["POST"], detail=True, url_path="review")
    def approve(self, request, pk):
        try:
            logging.getLogger().info("AdmissionRegistrationManagementView.approve pk=%s, req=%s", pk, request.data)
            validate = ReviewRegistrationValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            try:
                registration = AdmissionRegistration.objects.get(id=pk)

                if registration.is_reviewed:
                    return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Đơn đăng ký này đã được xét duyệt!").response
                
                if validate.validated_data["is_approve"]:
                    if not registration.is_passed:
                        return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Đơn đăng ký không đủ điều kiện xét duyệt!").response
                    
                    if registration.major.expected_target <= len(registration.major.admission_registrations.filter(review_status=ReviewStatusChoices.APPROVED)):
                        return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Đã vượt chỉ tiêu tuyển sinh cho ngành này!").response
                
                registration.reviewed_by = request.user
                registration.review_status = ReviewStatusChoices.APPROVED if validate.validated_data["is_approve"] else ReviewStatusChoices.REJECTED
                registration.save(update_fields=["reviewed_by", "review_status"])

                self.email_provider.send_html_template_email(
                    [registration.student.email],
                    [],
                    "[Trường Đại học Bình Dương] Thông Báo Kết Quả Xét Duyệt Đơn Xét Tuyển Đại Học 2024",
                    "approve_registration.html",
                    {
                        "student": registration.student,
                        "admission_registration": registration,
                        "created_at": registration.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                        "date_of_birth": registration.student.date_of_birth.strftime("%d/%m/%Y"),
                        "is_approved": registration.review_status == ReviewStatusChoices.APPROVED
                    }
                )

                messages = {
                    ReviewStatusChoices.APPROVED: f"Đơn xét tuyển ngành {registration.major.name} của học sinh {registration.student.fullname} đã được duyệt!",
                    ReviewStatusChoices.REJECTED: f"Đơn xét tuyển ngành {registration.major.name} của học sinh {registration.student.fullname} không đủ điều kiện xét duyệt!"
                }

                self.__create_approve_registration_noti_in_miniapp(
                    messages[ReviewStatusChoices.APPROVED],
                    registration.user
                )

                return RestResponse(status=status.HTTP_200_OK).response 
            except AdmissionRegistration.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            logging.getLogger().exception("AdmissionRegistrationManagementView.approve exc=%s, pk=%s, req=%s", e, pk, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def __create_approve_registration_noti_in_miniapp(self, content, user):
        try:
            noti = MiniappNotification(content=content, user=user)
            noti.save()
        except Exception as e:
            logging.getLogger().exception("AdmissionRegistrationManagementView.__create_approve_registration_noti_in_miniapp exc=%s, user=%s", e, user)
            