from rest_framework import serializers

from bduSuport.models.handbook import Handbook

class HandbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Handbook
        fields = "__all__"