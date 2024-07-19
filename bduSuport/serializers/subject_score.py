from rest_framework import serializers

from bduSuport.models.subject_score import SubjectScore

class SubjectScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectScore
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(set(existing) - set(fields)):
            self.fields.pop(field, None)

    def validate_score(self, value: float):
        s = str(value)
        _, decimal_places = s.split(".")

        if len(decimal_places) > 2:
            raise serializers.ValidationError("invalid_score_value")
        
        return value