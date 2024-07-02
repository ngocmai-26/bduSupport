import re
from rest_framework import serializers
from .create_academic import CreateAcademicValidator

class UpdateAcademicValidator(CreateAcademicValidator):
    name = serializers.CharField(max_length=255, required=False)