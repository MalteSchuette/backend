from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    """Custom JWT authentication that reads the access token from HTTP-only cookies."""

    def authenticate(self, request):
        """Extracts and validates the JWT token from the cookie."""
        access_token = request.COOKIES.get('access_token')
        if access_token is None:
            return None
        try:
            validated_token = self.get_validated_token(access_token)
            return self.get_user(validated_token), validated_token
        except (InvalidToken, TokenError):
            raise AuthenticationFailed('Invalid or expired token.')