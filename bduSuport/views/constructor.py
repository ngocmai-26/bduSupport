from rest_framework import viewsets, status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.response import RestResponse
from bduSuport.models.academic_level import AcademicLevel
from bduSuport.models.college_exam_group import CollegeExamGroup
from bduSuport.models.evaluation_method import EvaluationMethod
from bduSuport.models.major import Major
from bduSuport.serializers.academic_level import AcademicLevelSerializer
from bduSuport.serializers.college_exam_group import CollegeExamGroupSerializer
from bduSuport.serializers.evaluation_method_serializer import EvaluationMethodSerializer
from bduSuport.serializers.major_serializer import MajorSerializer
from bduSuport.models.miniapp_role import MiniappRole

class ConstructorView(viewsets.ViewSet):
    @action(methods=["GET"], detail=False, url_path="registration-form")
    def init_registration_form(self, request):
        try:
            data = {
                "evaluation_methods": self.__get_evaluation_methods(),
                "academic_levels": self.__get_academic_levels(),
                "college_exam_groups": self.__get_college_exam_groups(),
                "majors": self.__get_majors(),
            }
            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"ConstructorView.init_registration_form exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def __get_evaluation_methods(self):
        methods = EvaluationMethod.objects.all()
        return EvaluationMethodSerializer(methods, many=True, fields=["code", "name"]).data
    
    def __get_academic_levels(self):
        levels = AcademicLevel.objects.all()
        return AcademicLevelSerializer(levels, many=True, fields=["id", "name"]).data

    def __get_college_exam_groups(self):
        groups = CollegeExamGroup.objects.filter(deleted_at=None)
        return CollegeExamGroupSerializer(groups, many=True, fields=["id", "code", "name"]).data
    
    def __get_majors(self):
        majors = Major.objects.filter(deleted_at=None)
        return MajorSerializer(majors, many=True, fields=["code", "name"]).data
    
    @action(methods=["GET"], detail=False, url_path="feedback-form")
    def init_feedback_form(self, request):
        try:
            data = {
                "role": [
                    {
                        "name": "Học sinh",
                        "code": MiniappRole.STUDENT
                    },
                    {
                        "name": "Phụ huynh",
                        "code": MiniappRole.PARENT
                    },
                    {
                        "name": "Cựu sinh viên",
                        "code": MiniappRole.FORMER_STUDENT
                    }
                ],
            }
            return RestResponse(data=data, status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"ConstructorView.init_feedback_form exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response