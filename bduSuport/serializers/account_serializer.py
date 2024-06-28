from rest_framework.serializers import ModelSerializer
from ..models.account_model import Account

class AccountSerializer(ModelSerializer):
    class Meta: 
        model = Account
        fields = ['id', 'email', 'phone', 'password']