from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from bduSuport.models.academic_level import AcademicLevel
from bduSuport.models.evaluation_method import EvaluationMethod
from bduSuport.serializers.academic_level_serializer import AcademicLevelSerializer
from bduSuport.serializers.evaluation_method_serializer import EvaluationMethodSerializer

class ConstructorView(viewsets.ViewSet):
    @action(methods=["GET"], detail=False, url_path="registration-form")
    def init_registration_form(self, request):
        try:
            data = {
                "evaluation_methods": self.__get_evaluation_methods(),
                "academic_levels": self.__get_academic_levels()
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"ConstructorView.init_registration_form exc={e}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def __get_evaluation_methods(self):
        methods = EvaluationMethod.objects.all()
        return EvaluationMethodSerializer(methods, many=True).data
    
    def __get_academic_levels(self):
        methods = AcademicLevel.objects.all()
        return AcademicLevelSerializer(methods, many=True).data