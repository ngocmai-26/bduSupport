from rest_framework import viewsets, status
from rest_framework.decorators import action

from bduSuport.helpers.response import RestResponse

from bduSuport.middlewares.permissions.is_root import IsRoot
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication

from bduSuport.models.account import Account, AccountStatus


class BackofficeAccountManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )
    permission_classes = (IsRoot, )

    @action(methods=["GET"], detail=True, url_path="lock")
    def lock_account(self, request, pk):
        try:
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
            print(e)
            return RestResponse(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    @action(methods=["GET"], detail=True, url_path="unlock")
    def unlock_account(self, request, pk):
        try:
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
            print(e)
            return RestResponse(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR).response