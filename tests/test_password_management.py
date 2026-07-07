"""Tests for password management endpoints."""
from __future__ import annotations

from datetime import timedelta
from typing import Any, cast

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.authentication.models import PasswordResetToken
from apps.authentication.tokens import generate_reset_token


class PasswordManagementTests(APITestCase):
    """Test password reset and change flows."""

    def setUp(self) -> None:
        super().setUp()
        User = get_user_model()
        self.user = cast(Any, User.objects).create_user(
            username="testuser",
            email="test@example.com",
            password="OldPassword123!",
        )

    def test_forgot_password_generates_token(self) -> None:
        response = self.client.post(
            "/api/v1/auth/forgot-password/",
            {"email": "test@example.com"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            PasswordResetToken.objects.filter(user=self.user, is_used=False).exists(),
        )

    def test_reset_password_with_valid_token(self) -> None:
        token, hashed = generate_reset_token()
        PasswordResetToken.objects.create(
            user=self.user,
            hashed_token=hashed,
            expires_at=timezone.now() + timedelta(minutes=30),
        )

        response = self.client.post(
            "/api/v1/auth/reset-password/",
            {
                "token": token,
                "password": "NewPassword123!",
                "confirm_password": "NewPassword123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPassword123!"))
        self.assertTrue(
            PasswordResetToken.objects.filter(user=self.user, is_used=True).exists(),
        )

    def test_change_password_requires_authentication(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/api/v1/auth/change-password/",
            {
                "old_password": "OldPassword123!",
                "new_password": "UpdatedPassword123!",
                "confirm_password": "UpdatedPassword123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("UpdatedPassword123!"))
