import logging
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, status
from rest_framework.decorators import action

from bduSuport.helpers.audit import audit_back_office
from bduSuport.helpers.response import RestResponse
from bduSuport.services.otp import OtpService
from bduSuport.models.account import Account, AccountStatus
from bduSuport.validations.change_password import ChangePasswordValidator
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication

class AdminAccountView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )
    otp_service = OtpService()
        
    @action(methods=["PATCH"], detail=False, url_path="change-password")
    @swagger_auto_schema(request_body=ChangePasswordValidator)
    def change_password(self, request):
        try:
            logging.getLogger().info("AdminAccountView.swagger_auto_schema req=%s", request.data)
            validate = ChangePasswordValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu!").response
            
            validated_data = validate.validated_data
            old_pass = validated_data["old_password"]
            new_pass = validated_data["new_password"]

            try:
                account = Account.objects.get(id=request.user.id)
                
                if account.status != AccountStatus.ACTIVATED:
                    return RestResponse(message="Tài khoản của bạn chưa được kích hoạt hoặc đã bị vô hiệu hóa!", status=status.HTTP_400_BAD_REQUEST).response
            
                if not account.check_password(old_pass):
                    return RestResponse(message="Mật khẩu hiện tại chưa chính xác!", status=status.HTTP_400_BAD_REQUEST).response
                else:
                    account.set_password(new_pass)
                    account.save()
                    audit_back_office(request.user, "Đổi mật khẩu", "")

                return RestResponse(status=status.HTTP_200_OK).response
            except Account.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response
        except Exception as e:
            logging.getLogger().exception("AdminAccountView.change_password exc=%s, req=%s", e, request.data)
            return RestResponse(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR).response