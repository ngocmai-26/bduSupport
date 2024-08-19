from rest_framework import serializers

from bduSuport.models.feedback import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"