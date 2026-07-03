"""Root URL configuration for the Enterprise Auth Service."""

from django.http import HttpRequest, JsonResponse
from django.urls import URLPattern, URLResolver, path


def health_check(request: HttpRequest) -> JsonResponse:
    """Application health endpoint."""
    return JsonResponse(
        {
            "status": "healthy",
            "service": "enterprise-auth-service",
        }
    )


urlpatterns: list[URLPattern | URLResolver] = [
    path("health/", health_check, name="health"),
]
