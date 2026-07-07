"""Utility functions for authentication module."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser

    User = AbstractBaseUser


def get_user_by_email(email: str) -> AbstractBaseUser | None:
    """
    Retrieve a user by email address.

    Args:
        email: Email address to search for.

    Returns:
        AbstractBaseUser: The user object if found, None otherwise.
    """
    User = get_user_model()
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None
