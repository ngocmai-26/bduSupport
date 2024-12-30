from rest_framework import viewsets, status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from bduSuport.models.account import Account
from bduSuport.helpers.response import RestResponse
from bduSuport.helpers.paginator import CustomPageNumberPagination
from bduSuport.middlewares.permissions.is_admin_or_root import IsAdminOrRoot
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.serializers.account_serializer import AccountSerializer

class AccountManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )
    permission_classes = (IsAdminOrRoot, )

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter("size", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ])
    def list(self, request):
        queryset = Account.objects.all().order_by("-created_at")

        paginator = CustomPageNumberPagination()
        queryset = paginator.paginate_queryset(queryset, request)
        data = AccountSerializer(queryset, many=True, exclude=["password"]).data
        
        return RestResponse(data=paginator.get_paginated_data(data), status=status.HTTP_200_OK).response