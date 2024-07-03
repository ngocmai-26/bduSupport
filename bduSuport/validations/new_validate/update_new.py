import re
from rest_framework import serializers

class UpdateNewValidator(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    link = serializers.CharField(required=False)
    type = serializers.IntegerField(required=False)
    # image = serializers.ImageField(upload_to='news/%Y/%m', default=None)
    
    