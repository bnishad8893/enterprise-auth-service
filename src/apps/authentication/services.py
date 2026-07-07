"""Business logic services for authentication module."""
from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import status

User = get_user_model()


class AuthenticationService:
    """
    Service class for handling authentication business logic.

    This class encapsulates all authentication-related operations,
    keeping views thin and maintainable.
    """

    @staticmethod
    def login(email: str, password: str) -> dict[str, Any]:
        """
        Authenticate a user with email and password.

        Args:
            email: User email address.
            password: User password.

        Returns:
            dict: Result dict with 'success', 'user', 'errors' keys.
        """
        errors: dict[str, list[str]] = {}

        # Validate inputs
        if not email:
            errors["email"] = ["Email is required."]
        if not password:
            errors["password"] = ["Password is required."]

        if errors:
            return {
                "success": False,
                "user": None,
                "errors": errors,
                "status_code": status.HTTP_400_BAD_REQUEST,
            }

        # Check if user exists with this email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return {
                "success": False,
                "user": None,
                "errors": {"email": ["No user found with this email."]},
                "status_code": status.HTTP_401_UNAUTHORIZED,
            }

        # Check if user is active
        if not user.is_active:
            return {
                "success": False,
                "user": None,
                "errors": {"user": ["This user account is inactive."]},
                "status_code": status.HTTP_403_FORBIDDEN,
            }

        # Check password
        if not check_password(password, user.password):
            return {
                "success": False,
                "user": None,
                "errors": {"password": ["Invalid password."]},
                "status_code": status.HTTP_401_UNAUTHORIZED,
            }

        # Update last login
        from django.utils import timezone

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        return {
            "success": True,
            "user": user,
            "errors": None,
            "status_code": status.HTTP_200_OK,
        }

    @staticmethod
    def verify_token(request: Any) -> dict[str, Any]:
        """
        Verify if a request has a valid token.

        Args:
            request: The HTTP request object.

        Returns:
            dict: Result dict with 'success' and 'user' keys.
        """
        if request.user and getattr(request.user, "is_authenticated", False):
            return {
                "success": True,
                "user": request.user,
            }
        return {
            "success": False,
            "user": None,
        }
