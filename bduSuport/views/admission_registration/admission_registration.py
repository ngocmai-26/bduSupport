from rest_framework import viewsets, status
from django.db import transaction, IntegrityError
from drf_yasg.utils import swagger_auto_schema

from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.models.mini_app_user import MiniAppUser
from bduSuport.validations.submit_admission_registration import SubmitAdmissionRegistration

from bduSuport.models.student import Student
from bduSuport.models.subject_score import SubjectScore
from bduSuport.models.evaluation_method import EvaluationMethods
from bduSuport.models.admission_registration import AdmissionRegistration
from bduSuport.models.competency_assessment_exam_score import CompetencyAssessmentExamScore

class AdmissionRegistrationView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )
    
    @swagger_auto_schema(request_body=SubmitAdmissionRegistration)
    def create(self, request):
        try:
            request.user = MiniAppUser.objects.get(id=1)
            validate = SubmitAdmissionRegistration(data=request.data)

            if not validate.is_valid():
                return RestResponse(data=validate.errors, status=status.HTTP_400_BAD_REQUEST, message="Vui lòng kiểm tra lại dữ liệu của bạn!").response
            
            _data = validate.validated_data

            with transaction.atomic():
                student = Student(**_data["student"])
                student.save()

                if student.id is None:
                    raise IntegrityError("create_student_failed")
                
                _subject_scores = _data.pop("subject_scores")
                _competency_assessment_exam_score = _data.pop("competency_assessment_exam_score")
                
                registration = AdmissionRegistration(**{**_data, "student": student, "user": request.user})
                registration.save()

                if registration.id is None:
                    raise IntegrityError("create_registration_failed")
                
                evaluation_method = EvaluationMethods(registration.evaluation_method.code)

                ok = False
                
                if evaluation_method == EvaluationMethods.FiveSemestersOfHighSchool: 
                    ok = self.__create_case_5_semesters_of_high_school(_subject_scores, registration)

                elif evaluation_method == EvaluationMethods.CompetencyAssessmentExam:
                    ok = self.__create_case_competency_assessment_exam_score(_competency_assessment_exam_score, registration)
                
                elif evaluation_method == EvaluationMethods.Grade_12:
                    ok = self.__create_case_grade_12(_subject_scores, registration)
                
                elif evaluation_method == EvaluationMethods.Grades_10_11_12:
                    ok = self.__create_case_grades_10_11_12(_subject_scores, registration)
                
                elif evaluation_method == EvaluationMethods.HighSchoolGraduationExam:
                    ok = self.__create_case_high_school_graduation_exam(_subject_scores, registration)

                if not ok:
                    raise IntegrityError("create_score_failed")
                
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            print(f"AdmissionRegistration.create exc={e}")
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def __create_case_competency_assessment_exam_score(self, data, regisation) -> bool:
        try:
            score = CompetencyAssessmentExamScore(score=data["score"], admission_registration=regisation)
            score.save()

            return score.id is not None
        except Exception as e:
            print(f"AdmissionRegistration.__create_case_competency_assessment_exam_score exc={e}")
            return False
        
    def __create_case_5_semesters_of_high_school(self, data, regisation) -> bool:
        scores = SubjectScore.objects.bulk_create([SubjectScore(**{**item, "admission_registration": regisation}) for item in data])
        ids = [score.id is not None for score in scores]
        return all(ids)

    def __create_case_grade_12(self, data, regisation) -> bool:
        scores = SubjectScore.objects.bulk_create([SubjectScore(**{**item, "admission_registration": regisation}) for item in data])
        ids = [score.id is not None for score in scores]
        return all(ids)

    def __create_case_grades_10_11_12(self, data, regisation) -> bool:
        scores = SubjectScore.objects.bulk_create([SubjectScore(**{**item, "admission_registration": regisation}) for item in data])
        ids = [score.id is not None for score in scores]
        return all(ids)

    def __create_case_high_school_graduation_exam(self, data, regisation) -> bool:
        scores = SubjectScore.objects.bulk_create([SubjectScore(**{**item, "admission_registration": regisation}) for item in data])
        ids = [score.id is not None for score in scores]
        return all(ids)