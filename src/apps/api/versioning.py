"""API versioning configuration."""
from __future__ import annotations

from rest_framework.versioning import URLPathVersioning


class APIVersioning(URLPathVersioning):
    """
    URL path based versioning for the API.

    Versions are specified as URL path parameters, e.g., /api/v1/resource/
    """

    valid_versions = ("v1", "v2", "v3")
    version_param = "version"
    invalid_version_message = "Invalid API version."
