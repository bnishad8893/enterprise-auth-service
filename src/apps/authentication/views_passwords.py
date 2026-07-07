"""Views for password management endpoints."""
from __future__ import annotations

from typing import cast

from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.serializers_passwords import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from apps.authentication.services_passwords import (
    ChangePasswordService,
    ForgotPasswordService,
    ResetPasswordService,
)

from ..api.responses import error_response, success_response


class ForgotPasswordAPIView(APIView):
    """Initiate forgot password flow."""

    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(errors=serializer.errors, message="Invalid request", status_code=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        ForgotPasswordService.request_reset(email, request_meta=request.META)

        # Always return generic success message
        return success_response(data={}, message="If an account with that email exists, a reset email has been sent.", status_code=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    """Reset a password using a token."""

    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(errors=serializer.errors, message="Invalid request", status_code=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data["token"]
        password = serializer.validated_data["password"]

        result = ResetPasswordService.reset_password(token, password)
        if not result.get("success"):
            return error_response(errors=result.get("errors", {}), message="Password reset failed", status_code=result.get("status_code", status.HTTP_400_BAD_REQUEST))

        return success_response(data={}, message="Password reset successful.", status_code=status.HTTP_200_OK)


class ChangePasswordAPIView(APIView):
    """Change password for authenticated user."""

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(errors=serializer.errors, message="Invalid request", status_code=status.HTTP_400_BAD_REQUEST)

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]
        user = cast(AbstractBaseUser, request.user)

        result = ChangePasswordService.change_password(user, old_password, new_password)
        if not result.get("success"):
            return error_response(errors=result.get("errors", {}), message="Change password failed", status_code=result.get("status_code", status.HTTP_400_BAD_REQUEST))

        return success_response(data={}, message="Password changed successfully.", status_code=status.HTTP_200_OK)
