from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.admission_registration import AdmissionRegistration
from bduSuport.serializers.admission_registration_serializer import AdmissionRegistrationSerializer
from bduSuport.validations.review_registration import ReviewRegistrationValidator

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
    
    @swagger_auto_schema(request_body=ReviewRegistrationValidator)
    @action(methods=["POST"], detail=True, url_path="review")
    def approve(self, request, pk):
        try:
            validate = ReviewRegistrationValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(status=status.HTTP_400_BAD_REQUEST).response
            
            try:
                registration = AdmissionRegistration.objects.get(id=pk)

                if registration.is_approved:
                    return RestResponse(status=status.HTTP_400_BAD_REQUEST).response 
                
                registration.reviewed_by = request.user
                registration.review_result = validate.validated_data["is_approve"]
                registration.save(update_fields=["reviewed_by", "review_result"])

                return RestResponse(status=status.HTTP_200_OK).response 
            
            except AdmissionRegistration.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            print(f"AdmissionRegistrationManagementView.approve exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response