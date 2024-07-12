from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.response import RestResponse
from bduSuport.models.academic_level import AcademicLevel
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.serializers.academic_level import AcademicLevelSerializer

class AcademicLevelView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(request_body=AcademicLevelSerializer(exclude=["deleted_at"]))
    def create(self, request):
        try:
            validate = AcademicLevelSerializer(data=request.data, exclude=["deleted_at"])

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST).response
            
            subject = AcademicLevel(name=validate.validated_data["name"])
            subject.save()

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"AcademicLevelView.create exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response