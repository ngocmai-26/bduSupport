from rest_framework import serializers
from bduSuport.models.reservation import Reservation
from bduSuport.serializers.major_serializer import MajorSerializer
from bduSuport.const.provinces import vietnam_provinces

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"

    major = MajorSerializer()
    province_name = serializers.SerializerMethodField()

    def get_province_name(self, obj: Reservation):
        return vietnam_provinces.get(obj.province, "")