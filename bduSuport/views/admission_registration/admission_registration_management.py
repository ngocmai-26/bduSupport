from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.db import transaction, IntegrityError
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.backoffice_authentication import BackofficeAuthentication
from bduSuport.models.admission_registration import AdmissionRegistration
from bduSuport.models.competency_assessment_exam_score import CompetencyAssessmentExamScore
from bduSuport.models.evaluation_method import EvaluationMethods
from bduSuport.models.mini_app_user import MiniAppUser
from bduSuport.models.student import Student
from bduSuport.models.subject_score import SubjectScore
from bduSuport.serializers.admission_registration_serializer import AdmissionRegistrationSerializer
from bduSuport.validations.submit_admission_registration import SubmitAdmissionRegistration

class AdmissionRegistrationManagementView(viewsets.ViewSet):
    # authentication_classes = (BackofficeAuthentication, )

    def list(self, request):
        try:
            registrations = AdmissionRegistration.objects.filter(recalled_at=None)
            data = AdmissionRegistrationSerializer(registrations, many=True).data

            return RestResponse(data=data, status=status.HTTP_200_OK).response 
        except Exception as e:
            print(f"AdmissionRegistrationManagementView.list exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response

    def retrieve(self, request, pk):
        try:
            try:
                registration = AdmissionRegistration.objects.get(id=pk)
                data = AdmissionRegistrationSerializer(registration).data
                return RestResponse(data=data, status=status.HTTP_200_OK).response 
            
            except AdmissionRegistration.DoesNotExist:
                return RestResponse(status=status.HTTP_404_NOT_FOUND).response 
        except Exception as e:
            print(f"AdmissionRegistrationManagementView.retrieve exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response