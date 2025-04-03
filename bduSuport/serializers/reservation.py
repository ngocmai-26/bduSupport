from rest_framework import serializers
from bduSuport.models.reservation import Reservation
from bduSuport.serializers.major_serializer import MajorSerializer

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"

    major = MajorSerializer()