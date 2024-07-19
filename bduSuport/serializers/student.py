from rest_framework.serializers import ModelSerializer

from bduSuport.models.student import Student

class StudentSerializer(ModelSerializer):
    class Meta: 
        model = Student
        fields = "__all__"
        
   