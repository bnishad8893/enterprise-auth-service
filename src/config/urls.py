"""URL configuration for the enterprise authentication service."""
from __future__ import annotations

from typing import Any

from django.urls import include, path

app_name = "config"

urlpatterns: list[Any] = [
    path("api/", include("apps.authentication.urls")),
]
