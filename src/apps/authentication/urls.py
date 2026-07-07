"""URL configuration for the authentication app.

Includes token endpoints and password management endpoints.
"""
from __future__ import annotations

from django.urls import include, path

from apps.authentication import urls_passwords

urlpatterns = [
    # Password management endpoints
    path("", include((urls_passwords.urlpatterns, "authentication.passwords"))),
]
