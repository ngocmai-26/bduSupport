import re
import datetime
from rest_framework import serializers
from ...models.academic_level_model import AcademicLevel
from ...models.major_model import Major
from .create_student import CreateStudentValidator

class UpdateStudentValidator(CreateStudentValidator):
    fullName = serializers.CharField(max_length=255, required=False)
    gender = serializers.IntegerField(default=0)
    dateOfBirth = serializers.DateField(required=False)
    phone = serializers.CharField(max_length=15, required=False)
    address = serializers.CharField(max_length=255, required=False)
    highSchool = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=255, required=False)
    examGroup = serializers.CharField(max_length=255, required=False) 
    academicLevelId = serializers.PrimaryKeyRelatedField(queryset=AcademicLevel.objects.all(), allow_null=False)
    major = serializers.PrimaryKeyRelatedField(queryset=Major.objects.all(), many=True, required=False)

   