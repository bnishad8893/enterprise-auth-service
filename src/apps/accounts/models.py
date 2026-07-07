"""Custom User model for the authentication service."""

from __future__ import annotations

from typing import ClassVar

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.common.models import SoftDeleteModel, TimestampModel, UUIDModel

from .managers import UserManager


class User(
    UUIDModel,
    TimestampModel,
    SoftDeleteModel,
    AbstractBaseUser,
    PermissionsMixin,
):
    """Application user authenticated via email."""

    email = models.EmailField(
        unique=True,
        db_index=True,
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS: ClassVar[list[str]] = []

    class Meta:
        db_table = "users"
        ordering = ("-created_at",)
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self) -> str:
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def short_name(self) -> str:
        """Return the preferred short display name."""
        if self.first_name:
            return self.first_name
        return self.email
