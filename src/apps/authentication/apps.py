"""Application configuration for the authentication app."""
from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """Configuration for the authentication application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.authentication"
    verbose_name = "Authentication"
