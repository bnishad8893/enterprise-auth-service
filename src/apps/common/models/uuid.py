"""UUID primary-key abstract model.

Provides a simple UUID `id` primary key to be reused across domain models.
This keeps model definitions consistent and avoids repeated boilerplate.
"""

from __future__ import annotations

import uuid

from django.db import models


class UUIDModel(models.Model):
    """Abstract model that provides a UUID primary key named ``id``.

    Notes:
    - `editable=False` prevents accidental changes in admin/forms.
    - Using `uuid.uuid4` as the default provides a cryptographically
      random identifier suitable for distributed systems.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:  # pragma: no cover - simple container
        abstract = True
