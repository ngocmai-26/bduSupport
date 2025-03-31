from rest_framework import serializers
from bduSuport.models.reservation import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"