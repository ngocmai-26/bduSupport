import logging
from drf_yasg import openapi
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.paginator import CustomPageNumberPagination
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.reservation import Reservation
from bduSuport.serializers.reservation import ReservationSerializer

class ReservationManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter("page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter("size", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ])
    def list(self, request):
        try:
            queryset = Reservation.objects.filter(deleted_at=None).order_by("created_at")
            paginator = CustomPageNumberPagination()
            queryset = paginator.paginate_queryset(queryset, request)
            data = ReservationSerializer(queryset, many=True).data

            return RestResponse(data=paginator.get_paginated_data(data), status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("ReservationManagementView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
