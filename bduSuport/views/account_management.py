from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from bduSuport.models.account import Account
from bduSuport.serializers.account_serializer import AccountSerializer

class AccountManagementView(viewsets.ViewSet):
    def list(self, request):
        queryset = Account.objects.all()

        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = AccountSerializer(paginated_queryset, many=True, exclude=["password"])
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            account = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(account)
        return Response(serializer.data)