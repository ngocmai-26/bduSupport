from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from bduSuport.services.otp import OtpService
from bduSuport.validations.auth_validate.verify_validate import VerifyRequestValidator
from bduSuport.models.account import Account, AccountStatus

class AdminAccountView(viewsets.ViewSet):
    otp_service = OtpService()

    @action(methods=["POST"], detail=False, url_path="verify")
    @swagger_auto_schema(request_body=VerifyRequestValidator)
    def verify_account(self, request):
        try:
            validate = VerifyRequestValidator(data=request.data)

            if not validate.is_valid():
                return Response(validate.errors, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = validate.validated_data
            email = validated_data["email"]
            otp = validated_data["otp"]
            
            if self.otp_service.verify_otp("verify_account", email, otp):
                return Response({"message": "Verification failed!"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                account = Account.objects.get(email=email)
                
                if account.status != AccountStatus.UNVERIFIED:
                    return Response({"message": "Invalid account status!"}, status=status.HTTP_400_BAD_REQUEST) 
            
                account.status = AccountStatus.ACTIVATED
                account.save(update_fields=["status"])

                return Response(status=status.HTTP_200_OK)
            except:
                return Response(validate.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)