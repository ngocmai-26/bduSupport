import re
from rest_framework import serializers

from bduSuport.models.miniapp_role import MiniappRole

class CreateFeedbackValidator(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    feedbacker_role = serializers.ChoiceField(choices=MiniappRole.values)
    phone_number = serializers.CharField(max_length=20)

    def validate_phone_number(self, value):
        if not bool(re.match(r"^[0-9\-\+]{9,15}$", value)):
            raise serializers.ValidationError("invalid_phone_number")
        
        return value