from rest_framework import serializers

class CreateAppFunctionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    icon = serializers.ImageField()
    is_show = serializers.BooleanField(default=True)
    disable_miniapp_user_hidden = serializers.BooleanField(default=False)
    order = serializers.IntegerField(min_value=0)
    direct_to = serializers.CharField(max_length=255)