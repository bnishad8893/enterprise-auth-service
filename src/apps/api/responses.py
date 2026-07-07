"""Standard API response helpers and utilities."""
from __future__ import annotations

from typing import Any

from rest_framework import status
from rest_framework.response import Response


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = status.HTTP_200_OK,
) -> Response:
    """
    Create a standard success response.

    Args:
        data: The response data payload. Defaults to None.
        message: A descriptive message. Defaults to "Success".
        status_code: HTTP status code. Defaults to 200.

    Returns:
        Response: A DRF Response with standardized format.
    """
    return Response(
        {
            "success": True,
            "message": message,
            "data": data or {},
        },
        status=status_code,
    )


def error_response(
    errors: Any = None,
    message: str = "An error occurred",
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Response:
    """
    Create a standard error response.

    Args:
        errors: Error details as dict or list. Defaults to None.
        message: A descriptive error message. Defaults to "An error occurred".
        status_code: HTTP status code. Defaults to 400.

    Returns:
        Response: A DRF Response with error format.
    """
    return Response(
        {
            "success": False,
            "message": message,
            "errors": errors or {},
        },
        status=status_code,
    )
