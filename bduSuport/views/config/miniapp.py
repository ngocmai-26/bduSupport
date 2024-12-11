import logging
from rest_framework.decorators import action
from rest_framework import viewsets, status

from bduSuport.helpers.response import RestResponse
from bduSuport.models.app_function import AppFunction
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.serializers.app_function import AppFunctionSerializer

class MiniAppConfigView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )

    def list(self, request):
        try:
            data = {
                "functions": self.__get_app_functions()
            }

            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("MiniAppConfigView.config exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def __get_app_functions(self):
        try:
            funcs = AppFunction.objects.filter(deleted_at=None, is_show=True).order_by("-order")
            data = AppFunctionSerializer(funcs, many=True).data
            return data
        except Exception as e:
            logging.getLogger().exception("MiniAppConfigView.__get_app_functions exc=%s", e)
            return None