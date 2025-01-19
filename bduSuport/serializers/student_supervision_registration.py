from rest_framework import serializers

from bduSuport.models.student_supervision_registration import StudentSupervisionRegistration

class StudentSupervisionRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSupervisionRegistration
        fields = "__all__"