from rest_framework import serializers

from bduSuport.models.business_recruitment import BusinessRecruitment

class BusinessRecruitmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessRecruitment
        fields = "__all__"