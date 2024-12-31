import logging
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.audit import audit_back_office
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.mini_app_user import MiniAppUser
from bduSuport.validations.create_miniapp_notification import CreateMiniappNotificationValidator
from bduSuport.models.miniapp_notification import MiniappNotification

class MiniappNotificationManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(request_body=CreateMiniappNotificationValidator)
    def create(self, request):
        try:
            logging.getLogger().info("MiniappNotificationManagementView.create req=%s", request.data)
            validate = CreateMiniappNotificationValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            miniapp_users = MiniAppUser.objects.all()
            content = validate.validated_data["content"]
            MiniappNotification.objects.bulk_create([MiniappNotification(content=content, user=user) for user in miniapp_users])
            audit_back_office(request.user, "Gửi thông báo", content)
            
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("MiniappNotificationManagementView.create exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response