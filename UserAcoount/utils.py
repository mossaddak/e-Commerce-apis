from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from typing import Dict

User = get_user_model()


# Generate and return JWT tokens
def get_tokens_for_user(user) -> Dict[str, str]:
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class TokenHelper:
    def create_token(self, user: User) -> (str, str):
        """
        @user take the user instance.
        @response -> return refresh token and access token.
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh), str(refresh.access_token)
