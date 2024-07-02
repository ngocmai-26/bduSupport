
import re
from rest_framework import serializers
from .create_account import CreateAccountValidator

class UpdateAccountValidator(CreateAccountValidator):
    email = serializers.EmailField(required=False) 
    phone = serializers.CharField(required=False)
    password = serializers.CharField(required=False)