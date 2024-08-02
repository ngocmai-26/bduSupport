from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.major import Major
from bduSuport.serializers.major_serializer import MajorSerializer
from bduSuport.validations.create_major import CreateMajorValidator
from bduSuport.validations.update_major import UpdateMajorValidator

class MajorView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )
    
    @swagger_auto_schema(request_body=CreateMajorValidator)
    def create(self, request):
        try:
            validate = CreateMajorValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            with transaction.atomic():
                _data = validate.validated_data
                college_exam_groups = _data.pop("college_exam_groups")
                evaluation_methods = _data.pop("evaluation_methods")
                major = Major(**_data)
                major.save()
                major.college_exam_groups.set(college_exam_groups)
                major.evaluation_methods.set(evaluation_methods)

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"MajorView.create exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def list(self, request):
        try:
            majors = Major.objects.filter(deleted_at=None)
            data = MajorSerializer(majors, many=True).data
            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"MajorView.list exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            try:
                major = Major.objects.get(code=pk)
                major.deleted_at = datetime.now().date()
                major.save(update_fields=["deleted_at"])
            except Major.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response
            
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"MajorView.delete exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
    
    @swagger_auto_schema(request_body=UpdateMajorValidator)
    def update(self, request, pk):
        try:
            validate = UpdateMajorValidator(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            with transaction.atomic():
                try:
                    major = Major.objects.get(code=pk, deleted_at=None)
                    _data = validate.validated_data
                    college_exam_groups = _data.pop("college_exam_groups", None)
                    evaluation_methods = _data.pop("evaluation_methods")

                    for k, v in _data.items():
                        setattr(major, k, v)

                    major.save()
                    
                    if college_exam_groups is not None:
                        major.college_exam_groups.set(college_exam_groups)

                    if evaluation_methods is not None:
                        major.evaluation_methods.set(evaluation_methods)

                except Major.DoesNotExist:
                    return RestResponse(status=status.HTTP_404_NOT_FOUND).response
            
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"MajorView.update exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response