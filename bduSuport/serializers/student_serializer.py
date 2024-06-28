from rest_framework.serializers import ModelSerializer
from ..models.students_model import Students

class StudentsSerializer(ModelSerializer):
    class Meta: 
        model = Students
        fields = ['id', 'fullName', 'gender', 'dateOfBirth', 'phone', 'address', 'highSchool', 'city', 'examGroup', 'academicLevelId', 'major']
        
   