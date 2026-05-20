from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer


class RegisterView(APIView):
    """Handles user registration."""
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """Creates a new user account."""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Handles user login and sets JWT cookies."""
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """Authenticates the user and returns JWT tokens as HTTP-only cookies."""
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        response = Response({
            'detail': 'Login successfully!',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_200_OK)
        response.set_cookie('access_token', access_token, httponly=True, samesite='Lax')
        response.set_cookie('refresh_token', refresh_token,
                            httponly=True, samesite='Lax')
        return response


class LogoutView(APIView):
    """Handles user logout and blacklists the refresh token."""

    def post(self, request):
        """Logs out the user and deletes all auth cookies."""
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({'detail': 'No refresh token found.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response({'detail': 'Token is invalid or expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        response = Response(
            {'detail': 'Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid.'})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class TokenRefreshView(APIView):
    """Handles refreshing the access token using the refresh token cookie."""

    def post(self, request):
        """Refreshes the access token and sets a new cookie."""
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({'detail': 'No refresh token found.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            response = Response({'detail': 'Token refreshed'})
            response.set_cookie('access_token', access_token,
                                httponly=True, samesite='Lax')
            return response
        except TokenError:
            return Response({'detail': 'Token is invalid or expired.'}, status=status.HTTP_401_UNAUTHORIZED)
