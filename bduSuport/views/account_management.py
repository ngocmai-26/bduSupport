from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from bduSuport.models.account import Account
from bduSuport.middlewares.permissions.is_admin_or_root import IsAdminOrRoot
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.serializers.account_serializer import AccountSerializer

class AccountManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )
    permission_classes = (IsAdminOrRoot, )
    

    def list(self, request):
        queryset = Account.objects.all()

        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = AccountSerializer(paginated_queryset, many=True, exclude=["password"])
        return paginator.get_paginated_response(serializer.data)