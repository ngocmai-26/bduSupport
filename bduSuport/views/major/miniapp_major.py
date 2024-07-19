from rest_framework import viewsets, status
from rest_framework.decorators import action

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.models.evaluation_method import EvaluationMethod
from bduSuport.models.major import Major
from bduSuport.serializers.college_exam_group import CollegeExamGroupSerializer
from bduSuport.serializers.evaluation_method_serializer import EvaluationMethodSerializer

class MiniappMajorView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )

    @action(methods=["GET"], detail=True, url_path="evaluation-methods")
    def get_evaluation_methods_by_acadmic_major(self, request, pk):
        try:
            methods = EvaluationMethod.objects.filter(majors__id=pk)
            data = EvaluationMethodSerializer(methods, many=True).data
            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"MiniappMajorView.get_evaluation_methods_by_acadmic_major exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    @action(methods=["GET"], detail=True, url_path="college-exam-groups")
    def get_college_exam_groups_by_acadmic_major(self, request, pk):
        try:
            try:
                groups = Major.objects.get(id=pk).college_exam_groups.all()
                data = CollegeExamGroupSerializer(groups, many=True).data
                return RestResponse(data=data, status=status.HTTP_200_OK).response
            except Major.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response
        except Exception as e:
            print(f"MiniappMajorView.get_college_exam_groups_by_acadmic_major exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response