import logging
import datetime
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.audit import audit_back_office
from bduSuport.models.contact import Contact
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.serializers.contact import ContactSerializer
from bduSuport.validations.create_contact import CreateContactValidator
from bduSuport.validations.update_contact import UpdateContactValidator

class ContactManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(request_body=CreateContactValidator)
    def create(self, request):
        try:
            logging.getLogger().info("ContactManagementView.create req=%s", request.data)
            validate = CreateContactValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            contact = Contact(**validate.validated_data)
            contact.save()

            if contact.id is None:
                return RestResponse(status=status.HTTP_400_BAD_REQUEST, message="Đã xảy ra lỗi trong quá trình tạo tin tức!").response
            audit_back_office(request.user, "Tạo liên hệ", f"{contact.name} - {contact.phone} - {contact.location.name}")
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("ContactManagementView.create exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def list(self, request):
        try:
            contact = Contact.objects.filter(deleted_at=None).order_by("created_at")
            data = ContactSerializer(contact, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("ContactManagementView.list exc=%s", e)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    @swagger_auto_schema(request_body=UpdateContactValidator)
    def partial_update(self, request, pk):
        try:
            logging.getLogger().info("ContactManagementView.update req=%s", request.data)
            validate = UpdateContactValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            try:
                contact = Contact.objects.get(id=pk)
            except Contact.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
            
            for k, v in validate.validated_data.items():
                setattr(contact, k, v)
            
            contact.save(update_fields=list(validate.validated_data.keys()))
            audit_back_office(request.user, "Cập nhật liên hệ", f"{contact.name} - {contact.phone} - {contact.location.name}")
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("ContactManagementView.update exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            logging.getLogger().info("ContactManagementView.destroy pk=%s", pk)
            try:
                contact = Contact.objects.get(id=pk)
                contact.deleted_at = datetime.datetime.now()
                contact.save(update_fields=["deleted_at"])
                audit_back_office(request.user, "Xóa liên hệ", f"{contact.name} - {contact.phone} - {contact.location.name}")
                
                return RestResponse(status=status.HTTP_200_OK).response 
            except Contact.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            logging.getLogger().exception("ContactManagementView.destroy exc=%s, pk=%s", e, pk)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response