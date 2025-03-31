import re
from rest_framework import serializers
from bduSuport.models.reservation import Reservation

class CreateReservationValidator(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        exclude = ["miniapp_user", "deleted_at"]
    
    email = serializers.EmailField()

    def validate_phone_number(self, value):
        phone_pattern = re.compile(r"^(?:\+)?[0-9]{6,14}$")
        if not phone_pattern.match(value):
            raise serializers.ValidationError("Invalid phone number!")
        
        return value
    
    def validate_zalo_phone_number(self, value):
        phone_pattern = re.compile(r"^(?:\+)?[0-9]{6,14}$")
        if not phone_pattern.match(value):
            raise serializers.ValidationError("Invalid phone number!")
        
        return value