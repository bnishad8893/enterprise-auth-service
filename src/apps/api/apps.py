"""Application configuration for the REST API app."""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Configuration for the api application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.api"
    verbose_name = "REST API"
