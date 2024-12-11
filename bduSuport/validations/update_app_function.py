from rest_framework import serializers

class UpdateAppFunctionSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=255)
    icon = serializers.ImageField(required=False)
    is_show = serializers.BooleanField(required=False)
    order = serializers.IntegerField(required=False, min_value=0)
    direct_to = serializers.CharField(required=False, max_length=255)