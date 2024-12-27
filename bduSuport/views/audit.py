import logging
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.backoffice_autdit_log import BackofficeAuditLog
from bduSuport.serializers.backoffice_audit_log import BackofficeAuditLogSerializer
from bduSuport.middlewares.permissions.is_root import IsRoot

class AuditLogView(viewsets.ViewSet):
    # authentication_classes = (BackofficeAuthentication, )
    # permission_classes = (IsRoot, )
    
    @action(methods=["GET"], detail=False, url_path="backoffice")
    def list_backoffice_audit_logs(self, request):
        try:
            queryset = BackofficeAuditLog.objects.all().order_by("-created_at")
            paginator = PageNumberPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            data = BackofficeAuditLogSerializer(paginated_queryset, many=True).data

            return RestResponse(data=paginator.get_paginated_response(data).data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("AuditLogView.list_backoffice_audit_logs exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response