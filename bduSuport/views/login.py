from rest_framework import status
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView
import logging

from bduSuport.errors.un_verified_exception import UnVerifiedException
from bduSuport.helpers.response import RestResponse
from bduSuport.services.mail import EmailService
from bduSuport.services.otp import OtpService

class TokenPairView(TokenObtainPairView):
    otp_service = OtpService()
    email_service = EmailService()
    
    def post(self, request: Request, *args, **kwargs):
        try:
            logging.getLogger().info("TokenPairView.post req=%s", request.data)
            response = super().post(request, *args, **kwargs)
            logging.getLogger().info("TokenPairView.post res=%s", response.data)

            return RestResponse(
                data={
                    **response.data
                },
                status=status.HTTP_200_OK
            ).response
        except serializers.ValidationError:
            return RestResponse(message="Dữ liệu đầu vào không hợp lệ!", status=status.HTTP_400_BAD_REQUEST).response
        
        except UnVerifiedException as _:
            _email = request.data["email"]
            _otp = self.otp_service.generate_otp(6, "verify_account", _email)
            self.__send_otp_mail(_email, _otp)
            return RestResponse(message="Tài khoản chưa được xác thực", code="account_unverify", status=status.HTTP_400_BAD_REQUEST).response
        
        except exceptions.AuthenticationFailed as _:
            return RestResponse(message="Thông tin tài khoản không chính xác!", status=status.HTTP_400_BAD_REQUEST).response
        
        except exceptions.PermissionDenied as _:
            return RestResponse(message="Tài khoản đã bị khóa!", status=status.HTTP_400_BAD_REQUEST).response
        

    def __send_otp_mail(self, email, otp):
        try:
            subject = 'Confirmation Code for Registration'
            message = f'Your confirmation code is: {otp}'
            recipient_list = [email]
            
            self.email_service.send_simple_mail(subject, message, recipient_list)
        except Exception as e:
            logging.getLogger().exception("TokenPairView.__send_otp_mail exc=%s", e)
        