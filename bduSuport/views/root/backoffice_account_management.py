import logging
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.permissions.is_root import IsRoot
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.account import Account, AccountStatus
from bduSuport.validations.reset_password import ResetPasswordValidator

class BackofficeAccountManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )
    permission_classes = (IsRoot, )

    @action(methods=["PATCH"], detail=True, url_path="reset-password")
    @swagger_auto_schema(request_body=ResetPasswordValidator)
    def reset_password(self, request, pk):
        try:
            logging.getLogger().info("BackofficeAccountManagementView.reset_password pk=%s, req=%s", pk, request.data)
            try:
                validate = ResetPasswordValidator(data=request.data)

                if not validate.is_valid():
                    return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu!").response
                
                account = Account.objects.get(id=pk)
                account.set_password(validate.validated_data["new_password"])
                account.save()

                return RestResponse(status=status.HTTP_200_OK).response
            except Account.DoesNotExist:
                return RestResponse(message="Tài khoản không tồn tại!", status=status.HTTP_404_NOT_FOUND).response
        except Exception as e:
            logging.getLogger().exception("BackofficeAccountManagementView.reset_password exc=%s, pk=%s", e, pk)
            return RestResponse(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR).response

    @action(methods=["GET"], detail=True, url_path="lock")
    def lock_account(self, request, pk):
        try:
            logging.getLogger().info("BackofficeAccountManagementView.lock_account pk=%s", pk)
            try:
                account = Account.objects.get(id=pk)
                
                if account.status == AccountStatus.BLOCKED:
                    return RestResponse(message="Tài khoản đã bị khóa!", status=status.HTTP_400_BAD_REQUEST).response
                
                account.status = AccountStatus.BLOCKED
                account.save(update_fields=["status"])

                return RestResponse(status=status.HTTP_200_OK).response
            except Account.DoesNotExist:
                return RestResponse(message="Tài khoản không tồn tại!", status=status.HTTP_404_NOT_FOUND).response
        except Exception as e:
            logging.getLogger().exception("BackofficeAccountManagementView.lock_account exc=%s, pk=%s", e, pk)
            return RestResponse(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    @action(methods=["GET"], detail=True, url_path="unlock")
    def unlock_account(self, request, pk):
        try:
            logging.getLogger().info("BackofficeAccountManagementView.unlock_account pk=%s", pk)
            try:
                account = Account.objects.get(id=pk)
                
                if account.status != AccountStatus.BLOCKED:
                    return RestResponse(message="Tài khoản đang trong trạng thái hoạt động!", status=status.HTTP_400_BAD_REQUEST).response
                
                account.status = AccountStatus.UNVERIFIED
                account.save(update_fields=["status"])

                return RestResponse(status=status.HTTP_200_OK).response
            except Account.DoesNotExist:
                return RestResponse(message="Tài khoản không tồn tại!", status=status.HTTP_404_NOT_FOUND).response
        except Exception as e:
            logging.getLogger().exception("BackofficeAccountManagementView.unlock_account exc=%s, pk=%s", e, pk)
            return RestResponse(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR).response