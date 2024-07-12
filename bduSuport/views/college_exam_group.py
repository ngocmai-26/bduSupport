from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from bduSuport.models.college_exam_group import CollegeExamGroup
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.serializers.college_exam_group import CollegeExamGroupSerializer

class CollegeExamGroupView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(request_body=CollegeExamGroupSerializer(exclude=["deleted_at"]))
    def create(self, request):
        try:
            validate = CollegeExamGroupSerializer(data=request.data, exclude=["deleted_at"])

            if not validate.is_valid():
                return Response(data=validate.errors, status=status.HTTP_400_BAD_REQUEST)
            
            subject = CollegeExamGroup(name=validate.validated_data["name"])
            subject.save()

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(f"SubjectView.create exc={e}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)