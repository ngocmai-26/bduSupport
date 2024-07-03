
import re
from rest_framework import serializers

class UpdateAccountValidator(serializers.Serializer):
    email = serializers.EmailField(required=False) 
    phone = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    is_code = serializers.CharField(required=False)