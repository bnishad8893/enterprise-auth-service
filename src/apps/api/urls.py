"""URL configuration for the REST API."""
from __future__ import annotations

from django.urls import path

from apps.api.views import HealthCheckView

app_name = "api"

urlpatterns = [
    path("v1/health/", HealthCheckView.as_view(), name="health-check"),
]
