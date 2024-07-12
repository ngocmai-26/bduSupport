from rest_framework.serializers import ModelSerializer
from ..models.evaluation_method import EvaluationMethod

class EvaluationMethodSerializer(ModelSerializer):
    class Meta: 
        model = EvaluationMethod
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(set(existing) - set(fields)):
            self.fields.pop(field, None)