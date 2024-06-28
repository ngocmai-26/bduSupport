from django.http import HttpResponse
from rest_framework import viewsets, permissions
from ..models.account_model import Account
from ..serializers.account_serializer import AccountSerializer
# Create your views here.

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    

    

def index(request):
    return HttpResponse("Hello My App")