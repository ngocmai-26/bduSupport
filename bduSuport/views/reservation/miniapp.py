from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
import logging

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.models.reservation import Reservation
from bduSuport.validations.create_reservation import CreateReservationValidator

class MiniappReservationView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )
        
    @swagger_auto_schema(request_body=CreateReservationValidator)
    def create(self, request):
        try:
            logging.getLogger().info("MiniappReservationView.create req=%s", request.data)
            validate = CreateReservationValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            reservation = Reservation(**validate.validated_data, miniapp_user=request.user)
            reservation.save()

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("MiniappReservationView.create exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response