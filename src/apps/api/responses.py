"""Shared API response helpers."""
from __future__ import annotations

from typing import Any

from rest_framework.response import Response


def success_response(
    data: dict[str, Any] | None = None,
    message: str | None = None,
    status_code: int = 200,
) -> Response:
    """Return a standardized success response."""
    payload: dict[str, Any] = {
        "success": True,
        "data": data or {},
    }
    if message is not None:
        payload["message"] = message

    return Response(payload, status=status_code)


def error_response(
    errors: dict[str, Any] | None = None,
    message: str | None = None,
    status_code: int = 400,
) -> Response:
    """Return a standardized error response."""
    payload: dict[str, Any] = {
        "success": False,
        "errors": errors or {},
    }
    if message is not None:
        payload["message"] = message

    return Response(payload, status=status_code)
