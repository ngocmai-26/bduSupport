from rest_framework import serializers

class CreateBusinessRecruimentValidator(serializers.Serializer):
    business_name = serializers.CharField()
    job_title = serializers.CharField()
    summary = serializers.CharField()
    banner = serializers.ImageField()
    post_url = serializers.URLField()