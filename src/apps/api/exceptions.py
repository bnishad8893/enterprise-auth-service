"""Custom exception handler for REST API."""
from __future__ import annotations

from typing import Any

from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def api_exception_handler(
    exc: Exception,
    context: dict[str, Any],
) -> Response | JsonResponse | None:
    """
    Custom exception handler for REST API.

    Handles DRF exceptions and Django exceptions, returning
    consistent JSON responses.

    Args:
        exc: The exception that was raised.
        context: Additional context information.

    Returns:
        Response, JsonResponse, or None for unhandled exceptions.
    """
    # Default DRF exception handler
    response = drf_exception_handler(exc, context)

    if response is not None:
        return response

    # Handle Django PermissionDenied
    if isinstance(exc, PermissionDenied):
        return JsonResponse(
            {
                "success": False,
                "message": "Permission denied",
                "errors": {"detail": str(exc)},
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    # Handle ValidationError
    if isinstance(exc, ValidationError):
        return JsonResponse(
            {
                "success": False,
                "message": "Validation error",
                "errors": exc.detail if hasattr(exc, "detail") else {"detail": str(exc)},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Handle NotAuthenticated
    if isinstance(exc, NotAuthenticated):
        return JsonResponse(
            {
                "success": False,
                "message": "Authentication required",
                "errors": {"detail": "Not authenticated"},
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # Handle AuthenticationFailed
    if isinstance(exc, AuthenticationFailed):
        return JsonResponse(
            {
                "success": False,
                "message": "Authentication failed",
                "errors": {"detail": str(exc)},
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # Return None for unhandled exceptions (Django will handle them)
    return None
