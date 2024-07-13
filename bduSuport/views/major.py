from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction

from bduSuport.helpers.response import RestResponse
from bduSuport.models.major import Major
from bduSuport.serializers.major_serializer import MajorSerializer
from bduSuport.validations.create_major import CreateMajorValidator

class MajorView(viewsets.ViewSet):
    @swagger_auto_schema(request_body=CreateMajorValidator)
    def create(self, request):
        try:
            validate = CreateMajorValidator(data=request.data)

            if not validate.is_valid():
                return Response(data=validate.errors, status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                _data = validate.validated_data
                college_exam_groups = _data.pop("college_exam_groups")
                major = Major(**_data)
                major.save()
                major.college_exam_groups.set(college_exam_groups)

            return RestResponse(status=status.HTTP_200_OK)
        except Exception as e:
            print(f"SubjectView.create exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def list(self, request):
        try:
            subjects = Major.objects.filter(deleted_at=None)
            data = MajorSerializer(subjects, many=True).data
            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"SubjectView.list exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response