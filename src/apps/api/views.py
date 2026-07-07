"""API views and endpoints."""
from __future__ import annotations

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.responses import success_response


class HealthCheckView(APIView):
    """
    Health check endpoint for the authentication service.

    This endpoint allows monitoring systems to check service availability.
    """

    permission_classes = ()
    authentication_classes = ()

    def get(self, request: Request) -> Response:
        """
        Check the health status of the service.

        Args:
            request: The HTTP request object.

        Returns:
            Response: Health status JSON response.
        """
        return success_response(
            data={
                "status": "healthy",
                "service": "enterprise-auth-service",
                "version": "1.0.0",
            },
            message="Service is healthy",
            status_code=status.HTTP_200_OK,
        )
