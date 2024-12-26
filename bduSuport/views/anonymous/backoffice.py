import logging
from drf_yasg.utils import swagger_auto_schema

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status

from bduSuport.helpers.email import send_html_template_email
from bduSuport.helpers.response import RestResponse
from bduSuport.serializers.email import EmailValidator
from bduSuport.models.account import Account, AccountStatus
from bduSuport.services.otp import OtpService
from bduSuport.validations.verify_backoffice_account import BackofficeVerifyAccountValidator

class BackofficeAnonymousUserView(ViewSet):
    otp_service = OtpService()

    @action(methods=["POST"], detail=False, url_path="verify")
    @swagger_auto_schema(request_body=BackofficeVerifyAccountValidator)
    def verify_account(self, request):
        try:
            logging.getLogger().info("AdminAccountView.verify_account req=%s", request.data)
            validate = BackofficeVerifyAccountValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu!").response
            
            validated_data = validate.validated_data
            email = validated_data["email"]
            otp = validated_data["otp"]
            
            if not self.otp_service.verify_otp("verify_account", email, otp):
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="OTP không chính xác hoặc đã hết hạn!").response

            try:
                account = Account.objects.get(email=email)
                
                if account.status != AccountStatus.UNVERIFIED:
                    return RestResponse(message="Không thể kích hoạt tài khoản đã được xác thực!", status=status.HTTP_400_BAD_REQUEST).response
            
                account.status = AccountStatus.ACTIVATED
                account.save(update_fields=["status"])

                return RestResponse(status=status.HTTP_200_OK).response
            except Account.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response

        except Exception as e:
            logging.getLogger().exception("AdminAccountView.verify_account exc=%s, req=%s", e, request.data)
            return RestResponse(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
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
            send_html_template_email.apply_async(
                kwargs={
                    "to": [email],
                    "subject": "[Trường Đại học Bình Dương] Mã xác thực của bạn!",
                    "template_name": "otp.html",
                    "context": {
                        "otp": otp
                    }
                }
            )
        except Exception as e:
            logging.getLogger().exception("TokenPairView.__send_otp_mail exc=%s", e)