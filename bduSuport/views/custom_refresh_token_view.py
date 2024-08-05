from rest_framework import status
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenRefreshView

from bduSuport.helpers.response import RestResponse

class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return RestResponse(data=response.data, status=status.HTTP_200_OK).response
        except Exception as e:
            print(e)
            return RestResponse(code="refresh_token_failed", message="Refresh token hết hạn hoặc không hợp lệ!", status=status.HTTP_400_BAD_REQUEST).response