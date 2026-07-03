"""Development settings for local development and debugging."""

from .base import *

DEBUG = True
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="dev-secret-key")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
INTERNAL_IPS = ["127.0.0.1"]

STATICFILES_DIRS = [BASE_DIR / "static"]
