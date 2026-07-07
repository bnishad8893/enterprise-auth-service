"""Serializers for authentication module."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser

    User: type[AbstractBaseUser] = get_user_model()


class UserSerializer(serializers.ModelSerializer[Any]):
    """
    Serializer for User model.

    Exposes only non-sensitive user information.
    """

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "first_name", "last_name", "is_staff")
        read_only_fields = ("id", "email", "is_staff")


class LoginSerializer(serializers.Serializer[Any]):
    """
    Serializer for login endpoint.

    Validates email and password for user authentication.
    """

    email = serializers.EmailField(
        required=True,
        write_only=True,
        help_text="User email address",
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
        help_text="User password",
    )

    def validate_email(self, value: str) -> str:
        """
        Validate email is provided.

        Args:
            value: Email address.

        Returns:
            str: Validated email.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Email cannot be empty.")
        return value.lower().strip()

    def validate_password(self, value: str) -> str:
        """
        Validate password is provided.

        Args:
            value: Password.

        Returns:
            str: Validated password.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Password cannot be empty.")
        return value


class LogoutSerializer(serializers.Serializer[Any]):
    """
    Serializer for logout endpoint.

    Accepts refresh token for token blacklisting.
    """

    refresh = serializers.CharField(
        required=True,
        write_only=True,
        help_text="Refresh token to blacklist",
    )

    def validate_refresh(self, value: str) -> str:
        """
        Validate refresh token is provided.

        Args:
            value: Refresh token.

        Returns:
            str: Validated token.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Refresh token cannot be empty.")
        return value
