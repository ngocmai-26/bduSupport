from rest_framework import serializers

class DateRangeFilter(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        self.__max_date_diff = kwargs.pop("max_date_diff", 31)
        super().__init__(instance, data, **kwargs)

    from_date = serializers.DateField()
    to_date = serializers.DateField()

    def validate(self, attrs):
        _attrs = super().validate(attrs)

        if _attrs["to_date"] < _attrs["from_date"] or (_attrs["to_date"] - _attrs["from_date"]).days > self.__max_date_diff:
            raise serializers.ValidationError("invalid date range!")
        
        return _attrs