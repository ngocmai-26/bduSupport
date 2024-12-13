from rest_framework import serializers
from bduSuport.models.app_function import AppFunction

class AppFunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppFunction
        fields = "__all__"

    is_show_in_home = serializers.SerializerMethodField()

    def get_is_show_in_home(self, obj: AppFunction):
        try:
            if obj.personal_app_functions.first() is None:
                return True
            
            return obj.personal_app_functions.first().is_show_in_home
        except Exception as e:
            return False