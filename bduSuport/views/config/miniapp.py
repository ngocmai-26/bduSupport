import logging
from django.db.models import Q
from rest_framework import viewsets, status

from bduSuport.helpers.response import RestResponse
from bduSuport.models.app_function import AppFunction
from bduSuport.models.personal_app_function import PersonalAppFunction
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.serializers.app_function import AppFunctionSerializer

class MiniAppConfigView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )

    def list(self, request):
        try:
            data = {
                "functions": self.__get_app_functions(request.user)
            }

            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("MiniAppConfigView.config exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def __get_app_functions(self, user):
        try:
            funcs = AppFunction.objects.filter(
                Q(deleted_at=None) &
                Q(is_show=True) &
                (
                    ~Q(personal_app_functions__isnull=False) |
                    Q(
                        personal_app_functions__is_show_in_home=True,
                        personal_app_functions__user=user
                    )
                )
            ).distinct().order_by("-order")

            data = AppFunctionSerializer(funcs, many=True, context={"user": user}).data

            return data
        except Exception as e:
            logging.getLogger().exception("MiniAppConfigView.__get_app_functions exc=%s", e)
            return None