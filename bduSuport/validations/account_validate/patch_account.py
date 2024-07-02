# bduSuport/validations/patch_account.py

import re
from rest_framework import serializers
from .create_account import CreateAccountValidator

class PatchAccountValidator(CreateAccountValidator):
    email = serializers.EmailField(required=False) 
    phone = serializers.CharField(required=False)
    password = serializers.CharField(required=False)


    def validate(self, data):
     
        if not any(data.values()):
            raise serializers.ValidationError("At least one field must be provided for partial update.")
        return data
