from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction

from bduSuport.helpers.response import RestResponse
from bduSuport.models.college_exam_group import CollegeExamGroup
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.serializers.college_exam_group import CollegeExamGroupSerializer
from bduSuport.validations.create_college_exam_group import CreateCollegeExamGroupValidator

class CollegeExamGroupView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(request_body=CreateCollegeExamGroupValidator)
    def create(self, request):
        try:
            validate = CreateCollegeExamGroupValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST).response
            
            with transaction.atomic():
                _data = validate.validated_data
                subjects = _data.pop("subjects")
                group = CollegeExamGroup(**_data)
                group.save()
                group.subjects.set(subjects)

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"SubjectView.create exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def list(self, request):
        try:
            subjects = CollegeExamGroup.objects.filter(deleted_at=None)
            data = CollegeExamGroupSerializer(subjects, many=True).data
            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"SubjectView.list exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response