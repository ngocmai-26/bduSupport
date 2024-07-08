import re
import bcrypt
from rest_framework import serializers
from django.core.cache import cache
from ...models.account import Account, AccountStatus


class VerifyRequestValidator(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)