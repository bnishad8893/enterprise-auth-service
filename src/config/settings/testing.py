"""Testing settings for automated test execution."""

from .base import *

DEBUG = False
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="test-secret-key")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
