"""Validators for authentication module."""
from __future__ import annotations

from typing import Any


def validate_email_format(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email address to validate.

    Returns:
        bool: True if email format is valid.
    """
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> dict[str, Any]:
    """
    Validate password strength.

    Args:
        password: Password to validate.

    Returns:
        dict: Validation result with 'valid' and 'errors' keys.
    """
    errors: list[str] = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")

    if not any(char.isupper() for char in password):
        errors.append("Password must contain at least one uppercase letter.")

    if not any(char.isdigit() for char in password):
        errors.append("Password must contain at least one digit.")

    return {"valid": len(errors) == 0, "errors": errors}
