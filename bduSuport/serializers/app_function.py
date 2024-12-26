from rest_framework import serializers
from bduSuport.models.app_function import AppFunction

class AppFunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppFunction
        fields = "__all__"

    is_show_in_home = serializers.SerializerMethodField()

    def get_is_show_in_home(self, obj: AppFunction):
        try:
            f = obj.personal_app_functions.filter(user=self.context.get("user", None)).first()
            
            if f is None:
                return True
            
            return f.is_show_in_home
        except Exception as e:
            return False