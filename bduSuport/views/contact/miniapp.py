import logging
from rest_framework import viewsets, status

from bduSuport.models.contact import Contact
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.serializers.contact import ContactSerializer

class ContactView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )

    def list(self, request):
        try:
            contact = Contact.objects.filter(deleted_at=None).order_by("created_at")
            data = ContactSerializer(contact, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("ContactMiniappView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response