"""URL configuration for the enterprise authentication service."""
from __future__ import annotations

from django.urls import include, path

app_name = "config"

urlpatterns = [
    path("api/", include("apps.api.urls")),
]
