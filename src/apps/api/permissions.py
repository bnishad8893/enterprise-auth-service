"""Reusable permission classes for REST API."""
from __future__ import annotations

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class AllowAuthenticated(BasePermission):
    """
    Allow access only to authenticated users.

    Denies access to anonymous users.
    """

    message = "This endpoint requires authentication."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """
        Check if the user is authenticated.

        Args:
            request: The HTTP request object.
            view: The API view being accessed.

        Returns:
            bool: True if user is authenticated, False otherwise.
        """
        return bool(
            request.user and getattr(request.user, "is_authenticated", False)
        )


class AllowAdmin(BasePermission):
    """
    Allow access only to admin/staff users.

    Denies access to non-admin users and anonymous users.
    """

    message = "This endpoint requires admin privileges."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """
        Check if the user is an admin.

        Args:
            request: The HTTP request object.
            view: The API view being accessed.

        Returns:
            bool: True if user is admin, False otherwise.
        """
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "is_staff", False)
        )


class ReadOnly(BasePermission):
    """
    Allow any read method, deny all write methods.

    Permits GET, HEAD, and OPTIONS requests but denies
    POST, PUT, PATCH, DELETE.
    """

    message = "Read-only access."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """
        Check if the request is a safe method.

        Args:
            request: The HTTP request object.
            view: The API view being accessed.

        Returns:
            bool: True for safe methods, False otherwise.
        """
        return request.method in ("GET", "HEAD", "OPTIONS")
