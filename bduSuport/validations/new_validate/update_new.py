import re
from rest_framework import serializers
from .create_new import CreateNewValidator

class UpdateNewValidator(CreateNewValidator):
    title = serializers.CharField(max_length=255, required=False)
    link = serializers.CharField(required=False)
    type = serializers.IntegerField(required=False)
    # image = serializers.ImageField(upload_to='news/%Y/%m', default=None)
    
    