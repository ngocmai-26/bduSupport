from django.db import models

from bduSuport.models.account import Account
from bduSuport.models.college_exam_group import CollegeExamGroup
from bduSuport.models.major import Major
from bduSuport.models.mini_app_user import MiniAppUser
from .evaluation_method import EvaluationMethod, EvaluationMethods
from bduSuport.models.student import Student

class ReviewStatusChoices(models.TextChoices):
    PENDING = "pending"
    REJECTED = "rejected"
    APPROVED = "approved"

class AdmissionRegistration(models.Model):
    class Meta:
        db_table = "admission_registration"

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(MiniAppUser, on_delete=models.CASCADE, related_name="admission_registrations")
    evaluation_method = models.ForeignKey(EvaluationMethod, on_delete=models.CASCADE, related_name="admission_registrations")  
    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name="admission_registrations")
    college_exam_group = models.ForeignKey(CollegeExamGroup, on_delete=models.CASCADE, related_name="admission_registrations", null=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="admission_registration")
    reviewed_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="admission_registration", null=True)
    review_status = models.CharField(max_length=20, choices=ReviewStatusChoices.choices, default=ReviewStatusChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    recalled_at = models.DateTimeField(null=True)

    @property
    def is_reviewed(self):
        return self.reviewed_by != None

    @property
    def final_score(self):
        method = EvaluationMethods(self.evaluation_method.code)

        return {
            EvaluationMethods.HighSchoolGraduationExam: self.__calc_high_school_graduation_exam_final_score,
            EvaluationMethods.CompetencyAssessmentExam: self.__calc_competency_assessment_exam_final_score,
            EvaluationMethods.Grades_10_11_12: self.__calc_grades_10_11_12_final_score,
            EvaluationMethods.Grade_12: self.__calc_grade_12_final_score,
            EvaluationMethods.FiveSemestersOfHighSchool: self.__calc_5_semesters_of_high_school_final_score,
        }[method]()

    def __calc_high_school_graduation_exam_final_score(self):
        return self.subject_scores.aggregate(total_scores=models.Sum('score'))["total_scores"]

    def __calc_competency_assessment_exam_final_score(self):
        return self.competency_assessment_exam_score.all()[0].score

    def __calc_grades_10_11_12_final_score(self):
        return self.subject_scores.values('subject').annotate(
            adjusted_score=models.Sum(
                models.Case(
                    models.When(grade=12, then=models.F('score') * 2),
                    default=models.F('score')
                )
            )/4
        ).aggregate(total_scores=models.Sum('adjusted_score'))["total_scores"]

    def __calc_grade_12_final_score(self):
        return self.subject_scores.aggregate(total_scores=models.Sum('score'))["total_scores"]

    def __calc_5_semesters_of_high_school_final_score(self):
        return self.subject_scores \
            .values_list('subject') \
            .annotate(max_score=models.Max('score')) \
            .aggregate(total_max_scores=models.Sum('max_score'))["total_max_scores"]
  
    @property
    def is_passed(self):
        method = EvaluationMethods(self.evaluation_method.code)

        if method == EvaluationMethods.CompetencyAssessmentExam:
            return self.final_score >= self.major.benchmark_competency_assessment_exam
        else:
            return self.final_score >= self.major.benchmark_30