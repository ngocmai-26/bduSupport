import logging
from drf_yasg.utils import swagger_auto_schema

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status

from bduSuport.helpers.response import RestResponse
from bduSuport.serializers.email import EmailValidator
from bduSuport.models.account import Account, AccountStatus
from bduSuport.services.mail import EmailService
from bduSuport.services.otp import OtpService

class BackofficeAnonymousUserView(ViewSet):
    otp_service = OtpService()
    email_service = EmailService()
    
    @action(methods=["POST"], detail=False ,url_path="resend-verify-otp")
    @swagger_auto_schema(request_body=EmailValidator)
    def resend_verify_otp(self, request):
        try:
            validate = EmailValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response

            _email = validate.validated_data["email"]
            user = Account.objects.get(email=_email)

            if user.status != AccountStatus.UNVERIFIED:
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Tài khoản đã được kích hoạt trước đó!").response
            
            _otp = self.otp_service.generate_otp(6, "verify_account", _email)
            self.__send_otp_mail(_email, _otp)

            return RestResponse(message="Thành công!").response
        except Account.DoesNotExist as e:
            return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Email này chưa được đăng ký!").response
        except Exception as e:
            logging.getLogger().exception("BackofficeAnonymousUserView.resend_verify_otp exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def __send_otp_mail(self, email, otp):
        try:
            subject = 'Confirmation Code for Registration'
            message = f'Your confirmation code is: {otp}'
            recipient_list = [email]
            
            self.email_service.send_simple_mail(subject, message, recipient_list)
        except Exception as e:
            logging.getLogger().exception("TokenPairView.__send_otp_mail exc=%s", e)