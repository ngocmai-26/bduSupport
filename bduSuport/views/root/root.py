from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, status
from rest_framework.decorators import action

from bduSuport.helpers.response import RestResponse

from bduSuport.middlewares.permissions.is_root import IsRoot
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication

from bduSuport.models.account import Account, AccountRole, AccountStatus
from bduSuport.validations.create_backoffice_account import CreateBackofficeAccountValidator


class RootView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )
    permission_classes = (IsRoot, )

    @action(methods=["POST"], detail=False, url_path="accounts")
    @swagger_auto_schema(request_body=CreateBackofficeAccountValidator)
    def create_account(self, request):
        try:
            validate = CreateBackofficeAccountValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            validated_data = validate.validated_data
            
            if Account.objects.filter(email=validated_data["email"]).exists():
                return RestResponse(data={"message": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST, message="Email đã được sử dụng bởi một tài khoản khác!").response
            
            _password: str = validated_data.pop("password")

            account = Account(**validated_data)
            account.set_password(_password)
            account.status = AccountStatus.UNVERIFIED
            account.role = AccountRole.ADMIN
            account.save() 
                
            if account.id is None:
                return RestResponse(message="Failed to create account.", status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
            
            return RestResponse(message="Account created successfully", status=status.HTTP_201_CREATED).response
        except Exception as e:
            print(e)
            return RestResponse(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR).response