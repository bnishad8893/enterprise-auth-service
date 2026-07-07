"""Timestamp mixin abstract model.

Provides `created_at` and `updated_at` fields. These are simple and
well-understood building blocks for domain entities and help support
auditing and ordering without coupling to business logic.
"""

from __future__ import annotations

from django.db import models


class TimestampModel(models.Model):
    """Abstract model adding `created_at` and `updated_at` timestamps.

    - `created_at` uses `auto_now_add` to record initial creation time.
    - `updated_at` uses `auto_now` to reflect last modification time.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:  # pragma: no cover - simple container
        abstract = True
