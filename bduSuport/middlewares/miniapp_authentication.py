from django.core.cache import cache
from ..models.mini_app_user import MiniAppUser
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed

class MiniAppAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            bearer_token = request.headers.get("Authorization", None)

            if bearer_token is None:
                raise NotAuthenticated("Missing token!")
            
            token = bearer_token.replace("Bearer ", "")
            session_data = cache.get(f"mini_app_session:access:{token}", default=None)

            if session_data is None:
                raise AuthenticationFailed("Verify token failed!")
            
            user = MiniAppUser.objects.get(mini_app_user_id=session_data["user_id"])
            
            return (user, token)
        except Exception as e:
            print(f"MiniAppAuthentication.authenticate Exception={e}")
            raise AuthenticationFailed("Verify token failed!")