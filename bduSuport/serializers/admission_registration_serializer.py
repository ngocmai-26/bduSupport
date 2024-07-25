from rest_framework import serializers
from bduSuport.models.admission_registration import AdmissionRegistration
from bduSuport.serializers.student import StudentSerializer

class AdmissionRegistrationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = AdmissionRegistration
        fields = "__all__"

    final_score = serializers.SerializerMethodField()
    is_passed = serializers.SerializerMethodField()
    student_info = serializers.SerializerMethodField()
    major_name = serializers.SerializerMethodField()
    academic_level_name = serializers.SerializerMethodField()
    college_exam_group_name = serializers.SerializerMethodField()
    college_exam_group_code = serializers.SerializerMethodField()
    evaluation_method_name = serializers.SerializerMethodField()

    def get_final_score(self, obj: AdmissionRegistration):
        return obj.final_score
    
    def get_is_passed(self, obj: AdmissionRegistration):
        return obj.is_passed
    
    def get_student_info(self, obj: AdmissionRegistration):
        return StudentSerializer(obj.student).data
    
    def get_major_name(self, obj: AdmissionRegistration):
        return obj.major.name
    
    def get_academic_level_name(self, obj: AdmissionRegistration):
        return obj.major.academic_level.name
    
    def get_college_exam_group_name(self, obj: AdmissionRegistration):
        if obj.college_exam_group:
            return obj.college_exam_group.name
        return None
    
    def get_college_exam_group_code(self, obj: AdmissionRegistration):
        if obj.college_exam_group:
            return obj.college_exam_group.code
        return None
    
    def get_evaluation_method_name(self, obj: AdmissionRegistration):
        return obj.evaluation_method.name