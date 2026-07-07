"""Token utilities for password reset.

Generate secure tokens and hash them for storage.
"""
from __future__ import annotations

import hashlib
import secrets


def generate_reset_token() -> tuple[str, str]:
    """Generate a secure token and its SHA-256 hex digest.

    Returns:
        Tuple[str, str]: (plaintext_token, hashed_hex_digest)
    """
    token = secrets.token_urlsafe(32)
    hashed = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return token, hashed


def hash_token(token: str) -> str:
    """Return SHA-256 hex digest of a token."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
