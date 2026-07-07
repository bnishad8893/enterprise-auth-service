"""Password management services.

All business logic for forgot/reset/change password flows lives here.
"""
from __future__ import annotations

from contextlib import suppress
from datetime import timedelta
from typing import Any

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.cache import cache
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from apps.authentication.models import PasswordResetToken
from apps.authentication.tokens import generate_reset_token, hash_token


class ForgotPasswordService:
    """Service to create password reset tokens and send emails."""

    RATE_LIMIT = 5  # attempts
    RATE_LIMIT_WINDOW = 60 * 60  # seconds
    TOKEN_EXPIRY_MINUTES = 30

    @staticmethod
    def request_reset(email: str, request_meta: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Create a password reset token and send email if user exists.

        Does not leak whether account exists. Returns success in all cases.
        """
        # Rate limit by email
        rl_key = f"pwd_reset_rl:{email}"
        attempts = cache.get(rl_key, 0)
        if attempts >= ForgotPasswordService.RATE_LIMIT:
            return {"success": True, "status_code": status.HTTP_200_OK}
        cache.set(rl_key, attempts + 1, ForgotPasswordService.RATE_LIMIT_WINDOW)

        # Try to find user; do not reveal non-existence
        from django.contrib.auth import get_user_model

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Always return success to avoid account enumeration
            return {"success": True, "status_code": status.HTTP_200_OK}

        # Generate token and store only hash
        token, hashed = generate_reset_token()
        expires_at = timezone.now() + timedelta(minutes=ForgotPasswordService.TOKEN_EXPIRY_MINUTES)

        PasswordResetToken.objects.create(
            user=user,
            hashed_token=hashed,
            expires_at=expires_at,
        )

        # Send email with reset URL (do not log token)
        reset_url = f"{getattr(settings, 'FRONTEND_URL', 'https://example.com')}/reset-password?token={token}"
        subject = "Password reset request"
        message = (
            f"You requested a password reset. Use the following link to reset your password. "
            f"The link expires in {ForgotPasswordService.TOKEN_EXPIRY_MINUTES} minutes.\n\n{reset_url}"
        )
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")

        with suppress(Exception):
            send_mail(subject, message, from_email, [email], fail_silently=True)

        return {"success": True, "status_code": status.HTTP_200_OK}


class ResetPasswordService:
    """Service to reset password using a reset token."""

    @staticmethod
    @transaction.atomic
    def reset_password(token: str, new_password: str) -> dict[str, Any]:
        """
        Reset user's password given a plaintext token and new password.

        Validates token, expiry and one-time use, then sets the new password,
        blacklists outstanding refresh tokens, and marks token used.
        """
        hashed = hash_token(token)

        try:
            prt = PasswordResetToken.objects.select_for_update().get(hashed_token=hashed)
        except PasswordResetToken.DoesNotExist:
            return {"success": False, "errors": {"token": ["Invalid token."]}, "status_code": status.HTTP_400_BAD_REQUEST}

        if prt.is_used:
            return {"success": False, "errors": {"token": ["Token already used."]}, "status_code": status.HTTP_400_BAD_REQUEST}

        if prt.expires_at < timezone.now():
            return {"success": False, "errors": {"token": ["Token expired."]}, "status_code": status.HTTP_400_BAD_REQUEST}

        user = prt.user
        if not getattr(user, "is_active", True):
            return {"success": False, "errors": {"user": ["User account inactive."]}, "status_code": status.HTTP_403_FORBIDDEN}

        # Set password using Django's set_password
        user.set_password(new_password)

        # Update optional password_changed_at field if present
        if hasattr(user, "password_changed_at"):
            user.password_changed_at = timezone.now()

        user.save()

        # Mark token used
        prt.mark_used()

        # Blacklist outstanding refresh tokens
        with suppress(Exception):
            for ot in OutstandingToken.objects.filter(user=user):
                with suppress(Exception):
                    BlacklistedToken.objects.get_or_create(token=ot)

        return {"success": True, "status_code": status.HTTP_200_OK}


class ChangePasswordService:
    """Service to change password for authenticated users."""

    @staticmethod
    @transaction.atomic
    def change_password(user: AbstractBaseUser, old_password: str, new_password: str) -> dict[str, Any]:
        """
        Change an authenticated user's password after validating the old password.
        """
        # Verify old password
        if not user.check_password(old_password):
            return {"success": False, "errors": {"old_password": ["Old password is incorrect."]}, "status_code": status.HTTP_400_BAD_REQUEST}

        if user.check_password(new_password):
            return {"success": False, "errors": {"new_password": ["New password must be different from the old password."]}, "status_code": status.HTTP_400_BAD_REQUEST}

        user.set_password(new_password)
        if hasattr(user, "password_changed_at"):
            from django.utils import timezone

            user.password_changed_at = timezone.now()

        user.save()

        # Blacklist outstanding refresh tokens
        with suppress(Exception):
            for ot in OutstandingToken.objects.filter(user=user):
                with suppress(Exception):
                    BlacklistedToken.objects.get_or_create(token=ot)

        return {"success": True, "status_code": status.HTTP_200_OK}
