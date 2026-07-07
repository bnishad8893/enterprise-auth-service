"""API views for authentication module."""
from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.responses import error_response, success_response
from apps.authentication.serializers import (
    LoginSerializer,
    LogoutSerializer,
    UserSerializer,
)
from apps.authentication.services import AuthenticationService

User = get_user_model()


class LoginAPIView(APIView):
    """
    API view for user login.

    Authenticates user with email and password, returns access and refresh tokens.
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        """
        Handle POST request for user login.

        Args:
            request: The HTTP request object.

        Returns:
            Response: Login response with tokens and user data.
        """
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return error_response(
                errors=serializer.errors,
                message="Invalid email or password. Please try again.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        # Use service for authentication logic
        result = AuthenticationService.login(email, password)

        if not result["success"]:
            return error_response(
                errors=result["errors"],
                message="Authentication failed",
                status_code=result["status_code"],
            )

        user = result["user"]

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        user_serializer = UserSerializer(user)

        return success_response(
            data={
                "access": str(access),
                "refresh": str(refresh),
                "user": user_serializer.data,
            },
            message="Login successful.",
            status_code=status.HTTP_200_OK,
        )


class TokenRefreshAPIView(APIView):
    """
    API view for refreshing access token.

    Accepts a refresh token and returns a new access token.
    """

    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        """
        Handle POST request for token refresh.

        Args:
            request: The HTTP request object.

        Returns:
            Response: Refresh response with new access token.
        """
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return error_response(
                errors={"refresh": ["Refresh token is required."]},
                message="Refresh token not provided",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token

            return success_response(
                data={
                    "access": str(access),
                    "refresh": str(refresh),
                },
                message="Token refreshed successfully.",
                status_code=status.HTTP_200_OK,
            )
        except (InvalidToken, TokenError) as e:
            return error_response(
                errors={"refresh": ["Invalid or expired refresh token."]},
                message=f"Token refresh failed: {e!s}",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )


class TokenVerifyAPIView(APIView):
    """
    API view for verifying access token.

    Verifies the current user is authenticated.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        """
        Handle POST request for token verification.

        Args:
            request: The HTTP request object.

        Returns:
            Response: Verification response.
        """
        try:
            result = AuthenticationService.verify_token(request)

            if result["success"]:
                user_serializer = UserSerializer(result["user"])
                return success_response(
                    data={
                        "valid": True,
                        "user": user_serializer.data,
                    },
                    message="Token is valid.",
                    status_code=status.HTTP_200_OK,
                )

            return error_response(
                errors={"token": ["Invalid token."]},
                message="Token is invalid",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            return error_response(
                errors={"token": [str(e)]},
                message="Token verification failed",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutAPIView(APIView):
    """
    API view for user logout.

    Blacklists the refresh token to prevent reuse.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request: Request) -> Response:
        """
        Handle POST request for user logout.

        Args:
            request: The HTTP request object.

        Returns:
            Response: Logout response.
        """
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return error_response(
                errors=serializer.errors,
                message="Invalid logout request",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        refresh_token = serializer.validated_data.get("refresh")

        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()

            return success_response(
                data={},
                message="Logout successful.",
                status_code=status.HTTP_200_OK,
            )
        except (InvalidToken, TokenError) as e:
            return error_response(
                errors={"refresh": ["Invalid or expired refresh token."]},
                message=f"Logout failed: {e!s}",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
