from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from bduSuport.errors.un_verified_exception import UnVerifiedException

class TokenPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        
            return Response(
                {
                    **response.data
                },
                status.HTTP_200_OK
            )
        except serializers.ValidationError:
            return Response({"message": "Dữ liệu đầu vào không hợp lệ!"}, status.HTTP_400_BAD_REQUEST)
        except UnVerifiedException as e:
            return Response({"message": "Tài khoản chưa được xác thực"}, status.HTTP_400_BAD_REQUEST)
        except exceptions.AuthenticationFailed as e:
            return Response({"message": "Thông tin tài khoản không chính xác!"}, status.HTTP_400_BAD_REQUEST)
        except exceptions.PermissionDenied as e:
            return Response({"message": "Tài khoản đã bị khóa!"}, status.HTTP_400_BAD_REQUEST)
        