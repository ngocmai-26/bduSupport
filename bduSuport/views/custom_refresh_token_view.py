from rest_framework import status
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenRefreshView
import logging

from bduSuport.helpers.response import RestResponse

class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs):
        try:
            logging.getLogger().info("CustomRefreshTokenView.post req=%s", request.data)
            response = super().post(request, *args, **kwargs)
            return RestResponse(data=response.data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().info("CustomRefreshTokenView.post exc=%s, req=%s", e, request.data)
            return RestResponse(code="refresh_token_failed", message="Refresh token hết hạn hoặc không hợp lệ!", status=status.HTTP_400_BAD_REQUEST).response