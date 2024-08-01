from rest_framework import viewsets, status
from rest_framework.decorators import action

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.admission_registration import AdmissionRegistration
from bduSuport.serializers.admission_registration_serializer import AdmissionRegistrationSerializer

class AdmissionRegistrationManagementView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    def list(self, request):
        try:
            registrations = AdmissionRegistration.objects.filter(recalled_at=None)
            data = AdmissionRegistrationSerializer(registrations, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response 
        except Exception as e:
            print(f"AdmissionRegistrationManagementView.list exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response

    def retrieve(self, request, pk):
        try:
            try:
                registration = AdmissionRegistration.objects.get(id=pk)
                data = AdmissionRegistrationSerializer(registration).data
                return RestResponse(data=data, status=status.HTTP_200_OK).response 
            
            except AdmissionRegistration.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            print(f"AdmissionRegistrationManagementView.retrieve exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    @action(methods=["GET"], detail=True, url_path="approve")
    def approve(self, request, pk):
        try:
            try:
                registration = AdmissionRegistration.objects.get(id=pk)

                if registration.is_approved:
                    return RestResponse(status=status.HTTP_400_BAD_REQUEST).response 
                
                registration.approve_by = request.user
                registration.save(update_fields=["approve_by"])

                return RestResponse(status=status.HTTP_200_OK).response 
            
            except AdmissionRegistration.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            print(f"AdmissionRegistrationManagementView.approve exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response