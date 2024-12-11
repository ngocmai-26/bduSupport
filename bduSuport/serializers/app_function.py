from rest_framework import serializers
from bduSuport.models.app_function import AppFunction

class AppFunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppFunction
        fields = "__all__"