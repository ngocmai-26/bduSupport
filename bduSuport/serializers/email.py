from rest_framework import serializers

class EmailValidator(serializers.Serializer):
    email = serializers.EmailField()