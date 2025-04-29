from rest_framework import serializers

class DateFilter(serializers.Serializer):
    date = serializers.DateField()