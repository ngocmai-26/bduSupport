from rest_framework import serializers

class SubmitStudentSupervisionRegistration(serializers.Serializer):
    student_code = serializers.CharField()
    citizen_id = serializers.CharField()
    birthday = serializers.DateField()