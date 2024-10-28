from rest_framework import viewsets, status
from django.db import transaction, IntegrityError
from drf_yasg.utils import swagger_auto_schema
import logging

from bduSuport.helpers.email import EmailProvider
from bduSuport.helpers.response import RestResponse
from bduSuport.middlewares.miniapp_authentication import MiniAppAuthentication
from bduSuport.models.mini_app_user import MiniAppUser
from bduSuport.models.miniapp_notification import MiniappNotification
from bduSuport.validations.submit_admission_registration import SubmitAdmissionRegistration

from bduSuport.models.student import Student
from bduSuport.models.subject_score import SubjectScore
from bduSuport.models.evaluation_method import EvaluationMethods
from bduSuport.models.admission_registration import AdmissionRegistration
from bduSuport.models.competency_assessment_exam_score import CompetencyAssessmentExamScore

class AdmissionRegistrationView(viewsets.ViewSet):
    authentication_classes = (MiniAppAuthentication, )
    email_provider = EmailProvider()
    
    @swagger_auto_schema(request_body=SubmitAdmissionRegistration)
    def create(self, request):
        try:
            logging.getLogger().info("AdmissionRegistrationView.create req=%s", request.data)
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
                
            self.__create_submit_registration_noti_in_miniapp(
                f"Đơn xét tuyển ngành {registration.major.name} của học sinh {registration.student.fullname} đã được ghi nhận!",
                registration.user
            )
                
            self.email_provider.send_html_template_email(
                    [registration.student.email],
                    [],
                    "[Trường Đại học Bình Dương] Ghi Nhận Đơn Xét Tuyển Đại Học 2024",
                    "submit_registration.html",
                    {
                        "student": registration.student,
                        "admission_registration": registration,
                        "created_at": registration.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                        "date_of_birth": registration.student.date_of_birth.strftime("%d/%m/%Y"),
                    }
                )
                
            return RestResponse(status=status.HTTP_200_OK).response
        except Exception as e:
            logging.getLogger().exception("AdmissionRegistration.create exc=%s, req=%s", e, request.data)
            return RestResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR).response
        
    def __create_case_competency_assessment_exam_score(self, data, registration) -> bool:
        try:
            score = CompetencyAssessmentExamScore(score=data["score"], admission_registration=registration)
            score.save()

            return score.id is not None
        except Exception as e:
            logging.getLogger().exception("AdmissionRegistration.__create_case_competency_assessment_exam_score exc=%s", e)
            return False
        
    def __create_case_5_semesters_of_high_school(self, data, registration) -> bool:
        scores = SubjectScore.objects.bulk_create([SubjectScore(**{**item, "admission_registration": registration}) for item in data])
        ids = [score.id is not None for score in scores]
        return all(ids)

    def __create_case_grade_12(self, data, registration) -> bool:
        scores = SubjectScore.objects.bulk_create([SubjectScore(**{**item, "admission_registration": registration}) for item in data])
        ids = [score.id is not None for score in scores]
        return all(ids)

    def __create_case_grades_10_11_12(self, data, registration) -> bool:
        scores = SubjectScore.objects.bulk_create([SubjectScore(**{**item, "admission_registration": registration}) for item in data])
        ids = [score.id is not None for score in scores]
        return all(ids)

    def __create_case_high_school_graduation_exam(self, data, registration) -> bool:
        scores = SubjectScore.objects.bulk_create([SubjectScore(**{**item, "admission_registration": registration}) for item in data])
        ids = [score.id is not None for score in scores]
        return all(ids)
    
    def __create_submit_registration_noti_in_miniapp(self, content, user):
        try:
            noti = MiniappNotification(content=content, user=user)
            noti.save()
        except Exception as e:
            logging.getLogger().exception("AdmissionRegistration.__create_submit_registration_noti_in_miniapp exc=%s, user=%s", e, user)