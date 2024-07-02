import re
from rest_framework import serializers
from .create_new import CreateNewValidator

class PatchNewValidator(CreateNewValidator):
    title = serializers.CharField(max_length=255, required=False)
    link = serializers.CharField(required=False)
    type = serializers.IntegerField(required=False)
    # image = serializers.ImageField(upload_to='news/%Y/%m', default=None)
    
    def validate(self, data):
     
        if not any(data.values()):
            raise serializers.ValidationError("At least one field must be provided for partial update.")
        return data