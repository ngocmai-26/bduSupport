from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction

from bduSuport.models.college_exam_group import CollegeExamGroup
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.validations.create_college_exam_group import CreateCollegeExamGroupValidator

class CollegeExamGroupView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(request_body=CreateCollegeExamGroupValidator)
    def create(self, request):
        try:
            validate = CreateCollegeExamGroupValidator(data=request.data)

            if not validate.is_valid():
                return Response(data=validate.errors, status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                _data = validate.validated_data
                subjects = _data.pop("subjects")
                group = CollegeExamGroup(**_data)
                group.save()
                group.subjects.set(subjects)

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(f"SubjectView.create exc={e}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)