import re
from rest_framework import serializers
from .create_major import CreateMajorValidator

class UpdateMajorValidator(CreateMajorValidator):
    name = serializers.CharField(max_length=255)
    industryCode = serializers.CharField(max_length=255)
    targets = serializers.CharField(max_length=255)
    combination = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    year = serializers.CharField(max_length=255)
    benchmark = serializers.CharField(max_length=255) 
    tuition = serializers.CharField(max_length=255)
    trainingLocation = serializers.CharField(max_length=255)