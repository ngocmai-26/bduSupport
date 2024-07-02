import re
import datetime
from rest_framework import serializers
from ...models.academic_level_model import AcademicLevel
from ...models.major_model import Major

class CreateStudentValidator(serializers.Serializer):
    fullName = serializers.CharField(max_length=255, required=True)
    gender = serializers.IntegerField(default=0)
    dateOfBirth = serializers.DateField(required=True)
    phone = serializers.CharField(max_length=15, required=True)
    address = serializers.CharField(max_length=255, required=True)
    highSchool = serializers.CharField(max_length=255, required=True)
    city = serializers.CharField(max_length=255, required=True)
    examGroup = serializers.CharField(max_length=255, required=True) 
    academicLevelId = serializers.PrimaryKeyRelatedField(queryset=AcademicLevel.objects.all(), allow_null=False)
    major = serializers.PrimaryKeyRelatedField(queryset=Major.objects.all(), many=True, required=True)

    def validate_phone(self, value):
        phone_regex = r'^\+?1?\d{9,15}$'
        if not re.match(phone_regex, value):
            raise serializers.ValidationError("Invalid phone number format.")
        return value

    def validate_dateOfBirth(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value
    