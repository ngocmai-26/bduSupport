from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from bduSuport.helpers.response import RestResponse
from bduSuport.services.otp import OtpService
from bduSuport.models.account import Account, AccountStatus
from bduSuport.validations.verify_backoffice_account import BackofficeVerifyAccountValidator

class AdminAccountView(viewsets.ViewSet):
    otp_service = OtpService()

    @action(methods=["POST"], detail=False, url_path="verify")
    @swagger_auto_schema(request_body=BackofficeVerifyAccountValidator)
    def verify_account(self, request):
        try:
            validate = BackofficeVerifyAccountValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu!").response
            
            validated_data = validate.validated_data
            email = validated_data["email"]
            otp = validated_data["otp"]
            
            if self.otp_service.verify_otp("verify_account", email, otp):
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="OTP không chính xác hoặc đã hết hạn!").response

            try:
                account = Account.objects.get(email=email)
                
                if account.status != AccountStatus.UNVERIFIED:
                    return RestResponse(message="Không thể kích hoạt tài khoản đã được xác thực!", status=status.HTTP_400_BAD_REQUEST).response
            
                account.status = AccountStatus.ACTIVATED
                account.save(update_fields=["status"])

                return RestResponse(status=status.HTTP_200_OK).response
            except:
                return RestResponse(data=validate.errors, status=status.HTTP_404_NOT_FOUND).response

        except Exception as e:
            print(e)
            return RestResponse(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR).response