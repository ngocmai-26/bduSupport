import re
from rest_framework import serializers

class CreateMajorValidator(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True)
    industryCode = serializers.CharField(max_length=255, required=True)
    targets = serializers.CharField(max_length=255, required=True)
    combination = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(max_length=255, required=True)
    year = serializers.CharField(max_length=255, required=True)
    benchmark = serializers.CharField(max_length=255, required=True) 
    tuition = serializers.CharField(max_length=255, required=True)
    trainingLocation = serializers.CharField(max_length=255, required=True)
    
    def validate_name(self, value):
        if not re.match(r'^[a-zA-Z0-9\s]+$', value):
            raise serializers.ValidationError("Name can only contain letters, numbers, and spaces.")
        return value

    def validate_industryCode(self, value):
        if not re.match(r'^[A-Z0-9]+$', value):
            raise serializers.ValidationError("Industry code can only contain uppercase letters and numbers.")
        return value

    def validate_combination(self, value):
        if not re.match(r'^[A-Za-z0-9,]+$', value):
            raise serializers.ValidationError("Combination can only contain letters, numbers, and commas.")
        return value

    def validate_year(self, value):
        if not re.match(r'^\d{4}$', value):
            raise serializers.ValidationError("Year must be a 4-digit number.")
        return value

    def validate_benchmark(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Benchmark must be between 0 and 100.")
        return value

    def validate_tuition(self, value):
        if value < 0:
            raise serializers.ValidationError("Tuition cannot be negative.")
        return value
