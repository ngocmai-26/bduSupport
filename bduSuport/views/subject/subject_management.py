from datetime import datetime
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.response import RestResponse
from bduSuport.models.subject import Subject
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.serializers.subject import SubjectSerializer

class SubjectView(viewsets.ViewSet):
    authentication_classes = (BackofficeAuthentication, )

    @swagger_auto_schema(request_body=SubjectSerializer(exclude=["deleted_at"]))
    def create(self, request):
        try:
            validate = SubjectSerializer(data=request.data, exclude=["deleted_at"])

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            subject = Subject(name=validate.validated_data["name"])
            subject.save()

            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"SubjectView.create exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def list(self, request):
        try:
            subjects = Subject.objects.filter(deleted_at=None)
            data = SubjectSerializer(subjects, many=True).data
            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"SubjectView.list exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def destroy(self, request, pk):
        try:
            try:
                subject = Subject.objects.get(id=pk, deleted_at=None)
                college_groups = subject.college_groups.filter(deleted_at=None)

                if college_groups.exists():
                    gr_name = ", ".join([f"'{group.code}'" for group in college_groups])
                    message = f"Không thể xóa môn học vì các khối ngành {gr_name} đang tham chiếu đến môn học này."
                    return RestResponse(status=status.HTTP_400_BAD_REQUEST, message=message).response
                
                subject.deleted_at = datetime.now()
                subject.save(update_fields=["deleted_at"])
                
                return RestResponse(status=status.HTTP_200_OK).response
            except Subject.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            print(f"SubjectView.destroy exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response