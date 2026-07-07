"""Password management serializers."""
from __future__ import annotations

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class ForgotPasswordSerializer(serializers.Serializer[dict[str, str]]):
    """Serializer for initiating a password reset."""

    email = serializers.EmailField(required=True, write_only=True)


class ResetPasswordSerializer(serializers.Serializer[dict[str, str]]):
    """Serializer for resetting password using a reset token."""

    token = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError({"password": ["Passwords do not match."]})

        password = attrs["password"]
        validate_password(password)
        return attrs


class ChangePasswordSerializer(serializers.Serializer[dict[str, str]]):
    """Serializer for authenticated password change."""

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        if attrs.get("new_password") != attrs.get("confirm_password"):
            raise serializers.ValidationError({"new_password": ["Passwords do not match."]})

        new_password = attrs["new_password"]
        validate_password(new_password)
        return attrs
