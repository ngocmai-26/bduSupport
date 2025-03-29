import logging
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework import viewsets, status

from bduSuport.helpers.response import RestResponse
from bduSuport.models.app_function import AppFunction
from bduSuport.models.personal_app_function import PersonalAppFunction
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.serializers.app_function import AppFunctionSerializer

class MiniappAppFunctionView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )

    def list(self, request):
        try:
            funcs = AppFunction.objects.filter(
                Q(deleted_at=None) &
                Q(is_show=True) &
                ~Q(disable_miniapp_user_hidden=False)
            ).distinct().order_by("-order")

            data = AppFunctionSerializer(funcs, many=True, context={"user": request.user}).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("MiniappAppFunctionView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    @action(methods=["GET"], detail=True, url_path="show-in-home/enable")
    def enable_show_in_home(self, request, pk):
        try:
            try:
                app_func = AppFunction.objects.get(id=pk)

                if app_func.disable_miniapp_user_hidden:
                    return RestResponse(message="Bạn không có quyền thực hiện hành động này!", status=status.HTTP_400_BAD_REQUEST).response
                
            except AppFunction.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
            
            try:
                personal_app_func = PersonalAppFunction.objects.get(app_function=app_func, user=request.user)
                personal_app_func.is_show_in_home = True
                personal_app_func.save()
            except PersonalAppFunction.DoesNotExist:
                PersonalAppFunction(
                    app_function=app_func,
                    user=request.user,
                    is_show_in_home=True
                ).save()

            return RestResponse(status=status.HTTP_200_OK).response 
        except Exception as e:
            logging.getLogger().exception("MiniappAppFunctionView.enable_show_in_home exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    @action(methods=["GET"], detail=True, url_path="show-in-home/disable")
    def disable_show_in_home(self, request, pk):
        try:
            try:
                app_func = AppFunction.objects.get(id=pk)

                if app_func.disable_miniapp_user_hidden:
                    return RestResponse(message="Bạn không có quyền thực hiện hành động này!", status=status.HTTP_400_BAD_REQUEST).response
            except AppFunction.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
            
            try:
                personal_app_func = PersonalAppFunction.objects.get(app_function=app_func, user=request.user)
                personal_app_func.is_show_in_home = False
            except PersonalAppFunction.DoesNotExist:
                personal_app_func = PersonalAppFunction(
                    app_function=app_func,
                    user=request.user,
                    is_show_in_home=False
                )

            personal_app_func.save()
            return RestResponse(status=status.HTTP_200_OK).response 
        except Exception as e:
            logging.getLogger().exception("MiniappAppFunctionView.disable_show_in_home exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response