from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.core.cache import cache
from ..models.account import Account

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            bearer_token = request.headers.get("Authorization", None)

            if bearer_token is None:
                raise NotAuthenticated("Missing token!")
            
            token = bearer_token.replace("Bearer ", "")

            user_id = AccessToken(token=token).payload.get("user_id", None)
            jti = AccessToken(token=token).payload["jti"]

            if not bool(cache.has_key(f"session:{user_id}:access:{jti}")):
                raise AuthenticationFailed("Verify token failed!")
            
            account = Account.objects.get(id=user_id)
            
            return (account, token)
        except Exception as e:
            print(f"CustomJWTAuthentication.authenticate err={e}")
            raise AuthenticationFailed("Verify token failed!")