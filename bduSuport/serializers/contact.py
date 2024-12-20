from rest_framework import serializers

from bduSuport.models.contact import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

    location_name = serializers.SerializerMethodField()

    def get_location_name(self, obj):
        return obj.location.name