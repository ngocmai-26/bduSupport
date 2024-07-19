from rest_framework import serializers

from bduSuport.models.college_exam_group import CollegeExamGroup
from bduSuport.models.evaluation_method import EvaluationMethod, EvaluationMethods
from bduSuport.models.major import Major
from bduSuport.models.subject_score import GradeChoices, SemesterChoices
from bduSuport.serializers.competency_assessment_exam_score_serializer import CompetencyAssessmentExamScoreSerializer
from bduSuport.serializers.student import StudentSerializer
from bduSuport.serializers.subject_score import SubjectScoreSerializer

class SubmitAdmissionRegistration(serializers.Serializer):
    evaluation_method = serializers.PrimaryKeyRelatedField(queryset=EvaluationMethod.objects.filter(deleted_at=None))
    major = serializers.PrimaryKeyRelatedField(queryset=Major.objects.filter(deleted_at=None))
    college_exam_group = serializers.PrimaryKeyRelatedField(queryset=CollegeExamGroup.objects.filter(deleted_at=None), allow_null=True)
    student = StudentSerializer()
    subject_scores = SubjectScoreSerializer(many=True, allow_empty=False, allow_null=True, exclude=["admission_registration"])
    competency_assessment_exam_score = CompetencyAssessmentExamScoreSerializer(allow_null=True, exclude=["admission_registration"])

    def validate(self, attrs):
        _evaluation_method = attrs["evaluation_method"]

        {
            EvaluationMethods.FiveSemestersOfHighSchool: self.__validate_5_semesters_of_high_school,
            EvaluationMethods.CompetencyAssessmentExam: self.__validate_competency_assessment_exam,
            EvaluationMethods.Grade_12: self.__validate_grade_12,
            EvaluationMethods.Grades_10_11_12: self.__validate_grades_10_11_12,
            EvaluationMethods.HighSchoolGraduationExam: self.__validate_high_school_graduation_exam,
        }[EvaluationMethods(_evaluation_method.code)](attrs)

        return attrs

    def __validate_5_semesters_of_high_school(self, attrs):
        scores = attrs["subject_scores"]

        if scores is None:
            raise serializers.ValidationError("score_is_null")
        
        college_exam_group = attrs["college_exam_group"]

        if college_exam_group is None:
            raise serializers.ValidationError("college_exam_group_is_null")
        
        major = attrs["major"]

        if college_exam_group not in major.college_exam_groups.all():
            raise serializers.ValidationError("invalid_college_exam_group_for_major")
        
        valid_subjects = list(college_exam_group.subjects.all())
        validate_obj = {}

        for score in scores:
            if score["subject"] not in validate_obj:
                validate_obj[score["subject"]] = {score["grade"]: {score["semester"]}}
            else:
                if score["grade"] in validate_obj[score["subject"]]:
                    if score["semester"] in validate_obj[score["subject"]][score["grade"]]:
                        raise serializers.ValidationError("invalid_subject_semester")
                    else:
                        validate_obj[score["subject"]][score["grade"]].add(score["semester"])
                else:
                    validate_obj[score["subject"]][score["grade"]] = {score["semester"]}
                
        for k, v in validate_obj.items():
            if k not in valid_subjects:
                raise serializers.ValidationError("invalid_subject_for_major")
            
            if set(v.keys()) != {10, 11, 12}:
                raise serializers.ValidationError("has_invalid_or_lack_of_grades_for_subject")

            for _k, _v in v.items():
                if (_k == 12 and _v != {1}) or (_k in (10, 11) and _v != {1, 2}):
                    raise serializers.ValidationError("has_invalid_or_lack_of_semester")
            
            valid_subjects.remove(k)
        
        if len(valid_subjects) != 0:
            raise serializers.ValidationError("lack_of_subject")

    def __validate_competency_assessment_exam(self, attrs):
        score = attrs["competency_assessment_exam_score"]

        if score is None:
            raise serializers.ValidationError("score_is_null")

    def __validate_grade_12(self, attrs):
        scores = attrs["subject_scores"]

        if scores is None:
            raise serializers.ValidationError("score_is_null")
        
        college_exam_group = attrs["college_exam_group"]

        if college_exam_group is None:
            raise serializers.ValidationError("college_exam_group_is_null")
        
        major = attrs["major"]

        if college_exam_group not in major.college_exam_groups.all():
            raise serializers.ValidationError("invalid_college_exam_group_for_major")
        
        valid_subjects = list(college_exam_group.subjects.all())
        validate_obj = {}

        for score in scores:
            if score["semester"] != SemesterChoices.SCHOOL_YEAR.value:
                raise serializers.ValidationError("invalid_subject_semester")

            if score["subject"] not in validate_obj:
                validate_obj[score["subject"]] = {score["grade"]}
            else:
                if score["grade"] in validate_obj[score["subject"]]:
                    raise serializers.ValidationError("existed_subject_grade")
                
                validate_obj[score["subject"]].add(score["grade"])

        for k, v in validate_obj.items():
            if k not in valid_subjects:
                raise serializers.ValidationError("invalid_subject_for_major")
            
            if v != {12}:
                raise serializers.ValidationError("has_invalid_grade_for_subject")
            
            valid_subjects.remove(k)
        
        if len(valid_subjects) != 0:
            raise serializers.ValidationError("lack_of_subject")

    def __validate_grades_10_11_12(self, attrs):
        scores = attrs["subject_scores"]

        if scores is None:
            raise serializers.ValidationError("score_is_null")
        
        college_exam_group = attrs["college_exam_group"]

        if college_exam_group is None:
            raise serializers.ValidationError("college_exam_group_is_null")
        
        major = attrs["major"]

        if college_exam_group not in major.college_exam_groups.all():
            raise serializers.ValidationError("invalid_college_exam_group_for_major")
        
        valid_subjects = list(college_exam_group.subjects.all())
        validate_obj = {}

        for score in scores:
            if score["semester"] != SemesterChoices.SCHOOL_YEAR.value:
                raise serializers.ValidationError("invalid_subject_semester")

            if score["subject"] not in validate_obj:
                validate_obj[score["subject"]] = {score["grade"]}
            else:
                if score["grade"] in validate_obj[score["subject"]]:
                    raise serializers.ValidationError("existed_subject_grade")
                
                validate_obj[score["subject"]].add(score["grade"])

        for k, v in validate_obj.items():
            if k not in valid_subjects:
                raise serializers.ValidationError("invalid_subject_for_major")

            if v != {10, 11, 12}:
                raise serializers.ValidationError("has_invalid_or_lack_of_grades_for_subject")
            
            valid_subjects.remove(k)
        
        if len(valid_subjects) != 0:
            raise serializers.ValidationError("lack_of_subject")

    def __validate_high_school_graduation_exam(self, attrs):
        scores = attrs["subject_scores"]

        if scores is None:
            raise serializers.ValidationError("score_is_null")
        
        college_exam_group = attrs["college_exam_group"]

        if college_exam_group is None:
            raise serializers.ValidationError("college_exam_group_is_null")
        
        major = attrs["major"]

        if college_exam_group not in major.college_exam_groups.all():
            raise serializers.ValidationError("invalid_college_exam_group_for_major")
        
        valid_subjects = list(college_exam_group.subjects.all())
        validate_obj = {}

        for score in scores:
            if score["semester"] != SemesterChoices.SCHOOL_YEAR.value:
                raise serializers.ValidationError("invalid_subject_semester")

            if score["subject"] not in validate_obj:
                validate_obj[score["subject"]] = {score["grade"]}
            else:
                if score["grade"] in validate_obj[score["subject"]]:
                    raise serializers.ValidationError("existed_subject_grade")
                
                validate_obj[score["subject"]].add(score["grade"])

        for k, v in validate_obj.items():
            if k not in valid_subjects:
                raise serializers.ValidationError("invalid_subject_for_major")
            
            if v != {0}:
                raise serializers.ValidationError("has_invalid_grade_for_subject")
            
            valid_subjects.remove(k)
        
        if len(valid_subjects) != 0:
            raise serializers.ValidationError("lack_of_subject")
        
    def validate_empty_values(self, data):
        ok, _data = super().validate_empty_values(data)

        _evaluation_method = _data.get("evaluation_method", None)

        if _evaluation_method is not None:
            if _evaluation_method in [EvaluationMethods.CompetencyAssessmentExam.value]:
                _data["subject_scores"] = None
                _data["college_exam_group"] = None
            elif _evaluation_method in [
                EvaluationMethods.FiveSemestersOfHighSchool.value,
                EvaluationMethods.Grade_12.value,
                EvaluationMethods.Grades_10_11_12.value,
                EvaluationMethods.HighSchoolGraduationExam.value
            ]:
                _data["competency_assessment_exam_score"] = None

        return ok, _data