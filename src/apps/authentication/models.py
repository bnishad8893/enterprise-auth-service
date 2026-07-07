"""Models for authentication module."""
from __future__ import annotations

import uuid
from typing import Any

from django.conf import settings
from django.db import models


class PasswordResetToken(models.Model):
    """Model to store hashed password reset tokens.

    Only the hashed token is stored to avoid storing plaintext secrets.
    """

    id: models.UUIDField[Any, Any] = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user: models.ForeignKey[Any, Any] = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens",
    )
    hashed_token: models.CharField[Any, Any] = models.CharField(max_length=128, db_index=True)
    created_at: models.DateTimeField[Any, Any] = models.DateTimeField(auto_now_add=True)
    expires_at: models.DateTimeField[Any, Any] = models.DateTimeField()
    used_at: models.DateTimeField[Any, Any] = models.DateTimeField(null=True, blank=True)
    is_used: models.BooleanField[Any, Any] = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = "authentication_passwordresettoken"
        indexes = (models.Index(fields=("user",), name="authentication_pass_user_idx"),)

    def mark_used(self) -> None:
        """Mark this token as used."""
        from django.utils import timezone

        self.is_used = True
        self.used_at = timezone.now()
        self.save(update_fields=["is_used", "used_at"])
